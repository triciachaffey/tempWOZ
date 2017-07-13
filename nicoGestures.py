import argparse
import time
import random
import sys
import almath
from naoqi import ALProxy

robotIP = 'nico.d.mtholyoke.edu'
PORT = 9559
count = 0
try:
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
except Exception,e:
	print "Could not create proxy to ALMotion"
	print "Error was: ",e
	sys.exit(1)
try:
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
except Exception, e:
	print "Could not create proxy to ALRobotPosture"
	print "Error was: ", e



#Stiffens joints, allows for movement when autonomous life is off
pNames = "Body"
pStiffnessLists = 1.0
pTimeLists = 1.0
motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

r_shpitch = 'RShoulderPitch'
r_shroll ='RShoulderRoll'
l_shoulder = ['LShoulderPitch', 'LShoulderRoll']
l_elbow = ['LElbowYaw', 'LElbowRoll']
r_elbow = ['RElbowYaw', 'RElbowRoll']
r_wrist = 'RWristYaw'
r_hand = 'RHand'
l_wrist = 'LWristYaw'
l_hand = 'LHand'
head = ['HeadYaw', 'HeadPitch']

times = [[0.5], [0.5]]

bodyParts = ["LElbowYaw", "LElbowRoll", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "LHand", "RElbowYaw", "RElbowRoll", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand"]

headAndBody = ["HeadYaw", "LElbowYaw", "LElbowRoll", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "LHand", "RElbowYaw", "RElbowRoll", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand"]

#Only addition here is HeadPitch - do we need headAndBody and fullBody?
fullBody = ["HeadYaw", "HeadPitch", "LElbowYaw", "LElbowRoll", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "LHand", "RElbowYaw", "RElbowRoll", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand"]

head = ["HeadYaw", "HeadPitch"]

#Crouch - called to return Nico to a neutral stance
def crouch():
	postureProxy.post.goToPosture("Crouch", 0.5) 

#this method may become obsolete when autonomous life is off
def faceForward():
	motionProxy.post.angleInterpolationWithSpeed(head, [-0.07674193382263184, -0.2915019989013672], 0.15)

# Turn Nico's head in increments of 15 degrees. Has a failsafe so head doesn't get over-turned. Can be called repeatedly for further rotation.
# video (including Face Forward) - https://youtu.be/vwiHzgLqZcY
def turnHeadLeft():
	existingAngle = float(str(motionProxy.getAngles("HeadYaw", True))[1:5])
	if existingAngle < 0.75:
		newAngle = existingAngle + 15.0*almath.TO_RAD
		motionProxy.post.angleInterpolationWithSpeed(head, [newAngle, 0.0], 0.15)
# video (including Face Forward) - https://youtu.be/TGJX9x7fodI
def turnHeadRight():
	existingAngle = float(str(motionProxy.getAngles("HeadYaw", True))[1:5])
	if existingAngle > -0.75:
		newAngle = existingAngle - 15.0*almath.TO_RAD
		motionProxy.post.angleInterpolationWithSpeed(head, [newAngle, 0.0], 0.15)

#shrug and shake head - https://www.youtube.com/watch?v=IkmGZBAMzMA&edit=vd
def shrug_and_shakehead():
	motionProxy.post.angleInterpolationWithSpeed(headAndBody, [-0.5, -2.0856685638427734, -1.0139319896697998, 1.0660879611968994, 0.5874800682067871,-1.6828398704528809, 0.8079999685287476, 2.0856685638427734, 0.9158401489257812, 0.8744220733642578,-0.2055978775024414, 1.5109480619430542,0.795199990272522], 0.45)
	motionProxy.post.angleInterpolationWithSpeed(headAndBody, [0.5, -2.0856685638427734, -1.0139319896697998, 1.0660879611968994, 0.5874800682067871,-1.6828398704528809, 0.8079999685287476, 2.0856685638427734, 0.9158401489257812, 0.8744220733642578,-0.2055978775024414, 1.5109480619430542,0.795199990272522], 0.45)
	motionProxy.post.angleInterpolationWithSpeed(headAndBody, [0.0, -1.1965618133544922, -0.650373935, 1.520152091, 0.193242073059, 0.08279395103454, 0.8047999739646, 1.34374213218688, 0.536942005157, 1.47728395462, -0.158043861389, 0.156425952911376, 0.7919999957084656], 0.45)
	#crouch()



#Yay - https://www.youtube.com/watch?v=WM_fojCRtKQ
'''
Old yay - not necessary?
'''
#def yay():
#	motionProxy.angleInterpolationWithSpeed(bodyParts, [-0.40041589736938477, -0.6258301734924316, -1.2042322158813477, 0.6841220855712891, 0.3220980167388916, 0.7516000270843506, -0.05373191833496094, 0.8115279674530029, -1.3468101024627686, -0.7793140411376953, 0.1779019832611084, 0.7747999429702759], 0.45)

# https://youtu.be/6yQybFUNlPc
def fistYay():
	motionProxy.post.angleInterpolationWithSpeed(fullBody, [0.16256213, -0.3359880447, -1.033957, -1.1013700962, 0.725540161132, -0.3141592741012, -0.845275, 0.7480000257, 1.3544800281, 0.49552392, 1.544779777526, -0.001575946807, 0.187106132, 0.7719999551773071], 0.45)
	#crouch()


#Shrugging - https://www.youtube.com/watch?v=NzedmtWZlUs
def shrug():
	motionProxy.post.angleInterpolationWithSpeed(bodyParts, [-2.0856685638427734, -1.0139319896697998, 1.0660879611968994, 0.5874800682067871,-1.6828398704528809, 0.8079999685287476, 2.0856685638427734, 0.9158401489257812, 0.8744220733642578,-0.2055978775024414, 1.5109480619430542,0.795199990272522], 0.45)
	#crouch()

#Waving hands - https://www.youtube.com/watch?v=WZByH9MK6k0
def wave_hand(): 
	for i in range(2):
		motionProxy.post.angleInterpolationWithSpeed(bodyParts, [-2.0856685638427734, -0.817579984664917, 1.7395141124725342, -0.010779857635498047, -1.5831298828125, 0.8079999685287476, 0.7117340564727783, 1.4005842208862305, -0.6948599815368652, -0.7210218906402588, -0.257753849029541, 0.795199990272522], 0.45)
		motionProxy.post.angleInterpolationWithSpeed(bodyParts, [-2.0856685638427734, -0.817579984664917, 1.7379801273345947, -0.01077985763549, -1.5831298828, 0.80799996852, 0.7055981159, 0.7624399662017, -0.67952013015747, -1.09071588516, -0.2608220577, 0.795199990272522], 0.45)
	#crouch()

#Head Yaw (Nodding - up and down) https://www.youtube.com/watch?v=omMlTgr6xJY
def head_yaw(): 
	for i in range(2):
		motionProxy.post.angleInterpolation(head, [0.0, -0.3], times, True)
		motionProxy.post.angleInterpolation(head, [0.0, 0.2], times, True)
	#crouch()

#Head Pitch (Shaking - left and right) https://www.youtube.com/watch?v=s54Vg4sfawE
def head_pitch(): 
	for i in range(2):	
		motionProxy.post.angleInterpolation(head, [-0.6, 0.0], times, True)
		motionProxy.post.angleInterpolation(head, [0.6, 0.0], times, True)
	motionProxy.post.angleInterpolation(head, [0.0, 0.0], times, True)
	#crouch()

#Raises hand - https://youtu.be/Xb228W3l3C4
def oneHandUp():
	motionProxy.post.angleInterpolationWithSpeed(bodyParts, [-1.2901358604, -0.627364158, 0.547595977, 0.13648414, -1.638353, 0.8051999807, 1.3284020, 0.4955239295, 1.4711480140, 0.0014920234, 0.187106132, 0.7919999957084656], 0.45)
	#crouch()

# https://youtu.be/BcgxWY9eHYk
def peace():
	motionProxy.post.angleInterpolationWithSpeed(bodyParts, [-1.75033, -1.33914005756, -0.220937, 0.010695934, 1.0890979, 0.805199, 1.357548117637, 0.55995202, 1.543245792, 0.013764142990, 0.187106132, 0.7919999957084656], 0.45)
	#crouch()


# These gestures are from Sam's fluid motions code.

def waveRight2():
	names = ["HeadYaw", "HeadPitch",
	       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
	       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
	angleLists  = [[0.0*almath.TO_RAD],
	             [0.0*almath.TO_RAD],
	             
	             [80.0*almath.TO_RAD],
	             [6.5*almath.TO_RAD],
	             [-46.8*almath.TO_RAD],
	             [-57.8*almath.TO_RAD],
	             [7.6*almath.TO_RAD],
	             [0],
	             
	             [2.3*almath.TO_RAD],
	             [-18.9*almath.TO_RAD],
	             [73.5*almath.TO_RAD, 112.5*almath.TO_RAD, 73.5*almath.TO_RAD, 112.5*almath.TO_RAD],
	             [86.2*almath.TO_RAD],
	             [-66.8*almath.TO_RAD],
	             [1]]


	timeLists   = [[0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5, 1.0, 1.5, 2.0],
	             [0.5],
	             [0.5],
	             [0.5]]

	isAbsolute  = True
	# the post is so it happens at the same time as the speech
	motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
	## tts.say("Hello! Nice to meet you.")
	time.sleep(1.0)
	#crouch()

def handsOnHips():
	names = ["HeadYaw", "HeadPitch",
	       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
	       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
	angleLists  = [[0.0*almath.TO_RAD],
	             [0.0*almath.TO_RAD],
	             
	             [75.0*almath.TO_RAD],
	             [27.0*almath.TO_RAD],
	             [-5.8*almath.TO_RAD],
	             [-86.8*almath.TO_RAD],
	             [0.6*almath.TO_RAD],
	             [0],
	             
	             [84.0*almath.TO_RAD],
	             [-29.9*almath.TO_RAD],
	             [18.5*almath.TO_RAD],
	             [79.2*almath.TO_RAD],
	             [1.8*almath.TO_RAD],
	             [0]]

	              

	#*almath.TO_RAD
	timeLists   = [[0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5]]
	isAbsolute  = True
	# the post is so it happens at the same time as the speech
	motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
	## tts.say("I think I know what to do!")
	time.sleep(1.0)
	#crouch()

def largeShrug():
	names = ["HeadYaw", "HeadPitch",
	       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
	       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
	angleLists  = [[0.0*almath.TO_RAD],
	             [0.0*almath.TO_RAD],
	             
	             [65.0*almath.TO_RAD, 65.0*almath.TO_RAD],
	             [-4.0*almath.TO_RAD, -4.0*almath.TO_RAD],
	             [-119.8*almath.TO_RAD, -119.8*almath.TO_RAD],
	             [-79.8*almath.TO_RAD, -79.8*almath.TO_RAD],
	             [-49.6*almath.TO_RAD, -49.6*almath.TO_RAD],
	             [1],
	             
	             [65.0*almath.TO_RAD, 65.0*almath.TO_RAD],
	             [4.0*almath.TO_RAD, 4.0*almath.TO_RAD],
	             [119.8*almath.TO_RAD, 119.8*almath.TO_RAD],
	             [79.8*almath.TO_RAD, 79.8*almath.TO_RAD],
	             [49.6*almath.TO_RAD, 49.6*almath.TO_RAD],
	             [1]]

	              

	#*almath.TO_RAD
	timeLists   = [[0.5],
	             [0.5],
	             
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5],

	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5, 1.5],
	             [0.5]]

	isAbsolute  = True
	# the post is so it happens at the same time as the speech
	motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
	## tts.say("I don't know how to solve it")
	time.sleep(1.0)
	#crouch()

def handOutLeft():
	names = ["HeadYaw", "HeadPitch",
	       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
	       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
	angleLists  = [[0.0*almath.TO_RAD],
	             [0.0*almath.TO_RAD],
	             
	             [62.1*almath.TO_RAD],
	             [-1.2*almath.TO_RAD],
	             [-110.7*almath.TO_RAD],
	             [-49.2*almath.TO_RAD],
	             [-69.8*almath.TO_RAD],
	             [1],
	             
	             [80.7*almath.TO_RAD],
	             [0.2*almath.TO_RAD],
	             [54.8*almath.TO_RAD],
	             [49.6*almath.TO_RAD],
	             [4.3*almath.TO_RAD],
	             [0]]

	timeLists   = [[0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [1.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5]]

	isAbsolute  = True
	# the post is so it happens at the same time as the speech
	motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
	## tts.say("She ran three kilometers")
	time.sleep(1.0)
	#crouch()

def handOutRight():
	names = ["HeadYaw", "HeadPitch",
	       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
	       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
	angleLists  = [[0.0*almath.TO_RAD],
	             [0.0*almath.TO_RAD],
	             
	             [79.8*almath.TO_RAD],
	             [5.1*almath.TO_RAD],
	             [-52.5*almath.TO_RAD],
	             [-46.8*almath.TO_RAD],
	             [-26.6*almath.TO_RAD],
	             [0],
	             
	             [66.5*almath.TO_RAD],
	             [4.5*almath.TO_RAD],
	             [109.5*almath.TO_RAD],
	             [66.1*almath.TO_RAD],
	             [71.8*almath.TO_RAD],
	             [1]]

	#*almath.TO_RAD
	timeLists   = [[0.5],
	             [0.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [1.5],
	             
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5],
	             [0.5]]

	isAbsolute  = True
	# the post is so it happens at the same time as the speech
	motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
	## tts.say("So in 18 minutes she will be 6 kilometers away.")
	time.sleep(1.0)
	#crouch()


def handOnChestLeft():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD],
                     [0.0*almath.TO_RAD],

                     [44.9*almath.TO_RAD],
                     [-11.5*almath.TO_RAD],
                     [-30.2*almath.TO_RAD],
                     [-86.5*almath.TO_RAD],
                     [-36.6*almath.TO_RAD],
                     [1],
                     
                     [79.8*almath.TO_RAD],
                     [-10.4*almath.TO_RAD],
                     [46.1*almath.TO_RAD],
                     [58.1*almath.TO_RAD],
                     [-7.6*almath.TO_RAD],
                     [0]]


      #*almath.TO_RAD
      timeLists   = [[0.5],
                     [0.5],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [1.0],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("I think I know the answer!")
      time.sleep(1.0)
      #crouch()

def handOnChestRight():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD],
                     [0.0*almath.TO_RAD],

                     [76.9*almath.TO_RAD],
                     [0.3*almath.TO_RAD],
                     [-44.3*almath.TO_RAD],
                     [-46.1*almath.TO_RAD],
                     [-12.9*almath.TO_RAD],
                     [0],
                     
                     [43.9*almath.TO_RAD],
                     [9.7*almath.TO_RAD],
                     [22.7*almath.TO_RAD],
                     [88.5*almath.TO_RAD],
                     [51.8*almath.TO_RAD],
                     [1]]


      #*almath.TO_RAD
      timeLists   = [[0.5],
                     [0.5],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [1.0],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("I think I know the answer!")
      time.sleep(1.0)
      #crouch()

def cheering():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD],
                     [0.0*almath.TO_RAD],

                     [56.2*almath.TO_RAD],
                     [-9.9*almath.TO_RAD, -18.0*almath.TO_RAD],
                     [-60.9*almath.TO_RAD, -65.9*almath.TO_RAD],
                     [-88.5*almath.TO_RAD],
                     [5.7*almath.TO_RAD],
                     [0, 1],
                     
                     [60.7*almath.TO_RAD],
                     [18.0*almath.TO_RAD, 11.9*almath.TO_RAD],
                     [66.7*almath.TO_RAD, 62.7*almath.TO_RAD],
                     [88.5*almath.TO_RAD],
                     [-21.8*almath.TO_RAD],
                     [0, 1]]

      timeLists   = [[0.5],
                     [0.5],
                     
                     [0.5],
                     [0.5, 1.5],
                     [0.5, 1.5],
                     [0.5],
                     [0.5],
                     [0.5, 1.0],
                     
                     [0.5],
                     [0.5, 1.5],
                     [0.5, 1.5],
                     [0.5],
                     [0.5],
                     [0.5, 1.0]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("We did it!")
      time.sleep(1.0)
      #crouch()

def lookAtNailsLeft():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD, 15.7*almath.TO_RAD],
                     [0.0*almath.TO_RAD, -17.4*almath.TO_RAD],
                     
                     [81.0*almath.TO_RAD, -8.9*almath.TO_RAD],
                     [8.0*almath.TO_RAD, 2.9*almath.TO_RAD],
                     [-45.0*almath.TO_RAD, -60.2*almath.TO_RAD],
                     [-60.0*almath.TO_RAD, -88.7*almath.TO_RAD],
                     [8.7*almath.TO_RAD, -56.6*almath.TO_RAD, 84.6*almath.TO_RAD],
                     [0, 1],
                     
                     [81.0*almath.TO_RAD],
                     [-7.0*almath.TO_RAD],
                     [45.0*almath.TO_RAD],
                     [60.0*almath.TO_RAD],
                     [-10.6*almath.TO_RAD],
                     [0]]

      timeLists   = [[0.5, 2.0],
                     [0.5, 2.0],
                     
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0, 3.0],
                     [0.5, 2.0],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("hum")
      time.sleep(1.0)
      #crouch()



def lookAtNailsRight():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD, -5.7*almath.TO_RAD],
                     [0.0*almath.TO_RAD, 17.4*almath.TO_RAD],
                     
                     [79.0*almath.TO_RAD],
                     [10.0*almath.TO_RAD],
                     [-47.0*almath.TO_RAD],
                     [-60.0*almath.TO_RAD],
                     [8.0*almath.TO_RAD],
                     [0],
                     
                     [81.0*almath.TO_RAD, 48.9*almath.TO_RAD],
                     [-7.0*almath.TO_RAD, -2.9*almath.TO_RAD],
                     [45.0*almath.TO_RAD, 60.2*almath.TO_RAD],
                     [60.0*almath.TO_RAD, 88.7*almath.TO_RAD],
                     [1.0*almath.TO_RAD, 56.6*almath.TO_RAD, -104.6*almath.TO_RAD],
                     [0, 1]]

      timeLists   = [[0.5, 2.0],
                     [0.5, 2.0],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0],
                     [0.5, 2.0, 3.0],
                     [0.5, 3.0]]
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("hum")
      time.sleep(1.0)
      #crouch()

def nodYes():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[0.0*almath.TO_RAD],
                     [11.3*almath.TO_RAD, -11.3*almath.TO_RAD, 11.3*almath.TO_RAD, -11.3*almath.TO_RAD, 0.0*almath.TO_RAD],

                     [80.9*almath.TO_RAD],
                     [8.3*almath.TO_RAD],
                     [-45.3*almath.TO_RAD],
                     [-60.4*almath.TO_RAD],
                     [8.7*almath.TO_RAD],
                     [0],
                     
                     [80.8*almath.TO_RAD],
                     [-8.4*almath.TO_RAD],
                     [45.1*almath.TO_RAD],
                     [60.1*almath.TO_RAD],
                     [-10.6*almath.TO_RAD],
                     [0]]


      #*almath.TO_RAD
      timeLists   = [[0.5],
                     [0.5, 1.0, 1.5, 2.0, 2.5],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [1.5],
                     
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5],
                     [0.5]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("Yes, I agree")
      time.sleep(1.0)


def shakeNo():
      names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw", "LHand",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
      angleLists  = [[18.3*almath.TO_RAD, -18.3*almath.TO_RAD, 18.3*almath.TO_RAD, -18.3*almath.TO_RAD, 0.0*almath.TO_RAD],
                    [0.0*almath.TO_RAD],

                    [80.9*almath.TO_RAD],
                    [8.3*almath.TO_RAD],
                    [-45.3*almath.TO_RAD],
                    [-60.4*almath.TO_RAD],
                    [8.7*almath.TO_RAD],
                    [0],
                     
                    [80.8*almath.TO_RAD],
                    [-8.4*almath.TO_RAD],
                    [45.1*almath.TO_RAD],
                    [60.1*almath.TO_RAD],
                    [-10.6*almath.TO_RAD],
                    [0]]


      #*almath.TO_RAD
      timeLists   = [[0.5, 1.0, 1.5, 2.0, 2.5],
                    [0.5],
                     
                    [0.5],
                    [0.5],
                    [0.5],
                    [0.5],
                    [0.5],
                    [1.5],
                     
                    [0.5],
                    [0.5],
                    [0.5],
                    [0.5],
                    [0.5],
                    [0.5]]
      
      isAbsolute  = True
      # the post is so it happens at the same time as the speech
      motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
      ## tts.say("I don't think that's right")
      time.sleep(1.0)





#Below are notes and maximum values (I think), as well as respective videos 
'''
Gesture ideas:
1. thinking, tapping chin
2. thumbs up? 
3. hands on waist
4. fist pump
5. raise hand
6. what do we add? one hand up 

aldebaran store for example gestures
'''
'''
#Right Shoulder Pitch (Negative: Up) https://www.youtube.com/watch?v=zFQqWGHqxQ8
motionProxy.angleInterpolation(r_shpitch, -1.5, times, True)

#Right Shoulder Pitch (Neg then Pos: Up & Down) https://www.youtube.com/watch?v=jb78fG954q4
motionProxy.angleInterpolation(r_shpitch, -1.5, times, True)
motionProxy.angleInterpolation(r_shpitch, 1.5, times, True)

#Right ShoulderRoll (Negative- Sideways outward) https://www.youtube.com/watch?v=jzMTBv5x-Rc
motionProxy.angleInterpolation(r_shroll, -1.2, times, True)

#Right Shoulder Roll (Positive - Sideways inward) https://www.youtube.com/watch?v=F8ugJ6PWt9o
motionProxy.angleInterpolation(r_shroll, 0.3, times, True)

#Left Shoulder Pitch (Negative - Up) https://www.youtube.com/watch?v=Nd6TB7j2Ac0
motionProxy.angleInterpolation(l_shoulder, [-1.5, 0.0], times, True)

#Left Shoulder Roll (Negative - Inward+up/ Pitch = 0) 
#https://www.youtube.com/watch?v=CzXTNI4nRF0
motionProxy.angleInterpolation(l_shoulder, [0.0, -0.3], times, True)

#Left Shoulder Roll (Positive - Outward and bottom side of the arm faces the front/ Pitch = 0)
# https://www.youtube.com/watch?v=hHbi7ZO0awc
motionProxy.angleInterpolation(l_shoulder, [0.0, 1.3], times, True)

#Left ElbowYaw (Negative - Elbow straightened up) 
#https://www.youtube.com/watch?v=A6RyAci6ebs
motionProxy.angleInterpolation(l_elbow, [-2.0, 0.0], times, True)

#Left Elbow Yaw (Positive) https://www.youtube.com/watch?v=2GCND9D89kw
motionProxy.angleInterpolation(l_elbow, [2.0, 0.0], times, True)

#Left Elbow Roll (Negative) https://www.youtube.com/watch?v=6tVxHzpNC5E
motionProxy.angleInterpolation(l_elbow, [0.0, -1.5], times, True)

#Left Elbow Roll (Smaller Negative) https://www.youtube.com/watch?v=kc1Z92exDXM
motionProxy.angleInterpolation(l_elbow, [0.0, -0.03], times, True)

#Right Elbow Roll (Smaller Positive) https://www.youtube.com/watch?v=4cvWsaNAYCA
motionProxy.angleInterpolation(r_elbow, [0.0, 0.03], times, True)

#Right Elbow Roll (Positive) https://www.youtube.com/watch?v=1ToWtcF_cac
motionProxy.angleInterpolation(r_elbow, [0.0, 1.5], times, True)

#Right Elbow Yaw (Negative) https://www.youtube.com/watch?v=5R0hp7wZf4g
motionProxy.angleInterpolation(r_elbow, [-2.0, 0.0], times, True)

#Right Elbow Yaw (Positive) https://www.youtube.com/watch?v=CkR06JESXDQ
motionProxy.angleInterpolation(r_elbow, [2.0, 0.0], times, True)

#Right Wrist (Negative) https://www.youtube.com/watch?v=ypQJ95UJjME
motionProxy.angleInterpolation(r_wrist, -1.8, times, True)

#Right Wrist (Postivie) https://www.youtube.com/watch?v=iQiJe999Jvs
motionProxy.angleInterpolation(r_wrist, 1.8, times, True)

#Left Wrist (Negative) https://www.youtube.com/watch?v=o8y0aUQ9fVQ
motionProxy.angleInterpolation(l_wrist, -1.8, times, True)

#Left Wrist (Positive) https://www.youtube.com/watch?v=rBVEEVNgqbg
motionProxy.angleInterpolation(l_wrist, 1.8, times, True)'''
