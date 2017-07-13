# wizard GUI
import nicoController as control
import time
import threading      # thread related (commented out) code at bottom
import argparse
from threading import Thread
import adialog_new as ad
from naoqi import ALProxy
import shlex, subprocess
from sys import executable
from subprocess import *
import nicoGestures as gesture


from Tkinter import *

#create the window
root = Tk()

#modify root window
root.title("Wizard GUI")
#sets the width/height of window
root.geometry("500x465")

def main():
	# Set up the current time to be able to create the file
	currtime = time.asctime( time.localtime(time.time()) )[4:16]
	currtime = currtime.replace(" ", "-")
	currtime = currtime.replace(":", "")
	
	# Create the filename using the date and time
	filename = "log{}.txt".format(currtime)

	# If the key has dialog associated with it, log it to the file
	def writeFile(key):
		if key != "22" and key != "23" and key != "0":
			currtime = time.asctime( time.localtime(time.time()) )
			f = open(filename, "a")
			f.write(currtime + " ")
			if key.isdigit():
				f.write(control.dialog[key] + "\n")
			else:
				f.write(key + "\n")
			f.close()
	
	# Call the movement/dialog option and then write any dialog to the file
	def call(code):
		cmd = str(code)
		control.sendCmd(cmd)
		writeFile(cmd)
	
	#Buttons for every built-in dialog option

	# greetings
	greetings = Label(root, text = "Greetings")
	greetings.grid(row = 0, column = 1)

	b1 = Button(root, text = 'Hello!', command = lambda: call(1), width = 17)
	b1.grid(row = 1,column = 0)

	b16 = Button(root, text = 'I\'m excited!', command = lambda: call(16), width = 17)
	b16.grid(row = 1,column = 1)

	b20 = Button(root, text = 'I want to solve this', command = lambda: call(20), width = 17)
	b20.grid(row = 1,column = 2)


	# prompting the user to go on
	goOn = Label(root, text = "Go On")
	goOn.grid(row = 2,column = 1)

	b18 = Button(root, text = 'Okay!', command = lambda: call(18), width = 17)
	b18.grid(row = 3)

	b2 = Button(root, text = 'How do you solve this?', command = lambda: call(2), width = 17)
	b2.grid(row = 3,column = 1)

	b5 = Button(root, text = 'What\'s next?', command = lambda: call(5), width = 17)
	b5.grid(row = 3,column = 2)

	b8 = Button(root, text = 'How do we do that?', command = lambda: call(8), width = 17)
	b8.grid(row = 4)

	b13 = Button(root, text = 'Nevermind, go on.', command = lambda: call(13), width = 17)
	b13.grid(row = 4,column = 1)

	# Math
	mathL = Label(root, text = "Math")
	mathL.grid(row = 5,column = 1)

	b3 = Button(root, text = 'We multiply?', command = lambda: call(3), width = 17)
	b3.grid(row = 6)

	b19 = Button(root, text = 'We divide?', command = lambda: call(19), width = 17)
	b19.grid(row = 6,column = 1)

	b4 = Button(root, text = 'We add?', command = lambda: call(4), width = 17)
	b4.grid(row = 6,column = 2)

	b21 = Button(root, text = 'How\'d we get that #?', command = lambda: call(21), width = 17)
	b21.grid(row = 7)

	# ask for explanation
	explain = Label(root, text = "Ask for explanation")
	explain.grid(row = 8,column = 1)

	b7 = Button(root, text = 'That was a lot.', command = lambda: call(7), width = 17)
	b7.grid(row = 9)

	b11 = Button(root, text = 'Seems complicated.', command = lambda: call(11), width = 17)
	b11.grid(row = 9,column = 1)

	b12 = Button(root, text = 'Explain that again?', command = lambda: call(12), width = 17)
	b12.grid(row = 9,column = 2)

	b15 = Button(root, text = 'Don\'t know. Hint?', command = lambda: call(15), width = 17)
	b15.grid(row = 10)

	# endro
	endL = Label(root, text = "End Interaction")
	endL.grid(row = 11,column = 1)

	b6 = Button(root, text = 'I understand now', command = lambda: call(6), width = 17)
	b6.grid(row = 12)

	b9 = Button(root, text = 'Solved the problem!', command = lambda: call(9), width = 17)
	b9.grid(row = 12,column = 1)

	b10 = Button(root, text = 'Thank you!', command = lambda: call(10), width = 17)
	b10.grid(row = 12,column = 2)

	b14 = Button(root, text = 'Getting tired. Later?', command = lambda: call(14), width = 17)
	b14.grid(row = 13)

	#Misc
	other = Label(root, text = "Other")
	other.grid(row = 14,column = 1)

	#b17 = Button(root, text = 'Green paint?', command = lambda: call(17), width = 17)
	#b17.grid(row = 15,column = 2)

	# Make Nico turn his head 
	b0 = Button(root, text = "Face forward", command = lambda: call(0), width = 17)
	b0.grid(row = 15)
	
	b22 = Button(root, text = "Turn Head Left", command = lambda: call(22), width = 17)
	b22.grid(row = 15, column = 1) 

	b23 = Button(root, text = "Turn Head Right", command = lambda: call(23), width = 17)
	b23.grid(row = 15, column = 2)


	# Enter anything for Nico to say
	eLabel =  Label(root,text = "Enter text:")
	eLabel.grid(row = 16)
	entry = Entry()
	entry.grid(row = 16,column = 1)

	eText = ""

	def onclick(event = None):
		eText = entry.get()
		call(eText)
		entry.delete(0,END)

	root.bind('<Return>', onclick)

	button = Button(root, text = "Enter", command = onclick, width = 17)
	button.grid(row = 16,column = 2)

	# End the program immediately.
	bEnd = Button(root, text = "End program", command = exit, width = 17, bg = 'red')
	bEnd.grid(row = 17, column = 1)

	#kick off the event loop
	root.mainloop()


# Below is messy (sorry)


# Tried setting up the thread from a method point of view (see link in threadControl for my reference)
# Was not successful (compiled, but no GUI popped up, nor did any print statements I dropped into the adialog main)
'''
if __name__ == "__main__":
	guiThread = Thread(target = main())
	dialogThread = Thread(target = ad.main())
	guiThread.setDaemon(True)
	dialogThread.setDaemon(True)
	guiThread.start()
	dialogThread.start()
	while True:
		pass
'''

# Below is the original code that was somewhat modified, but primarily left alone
# with the exception of uncommenting out lines related to the threading
# The issue I found with this one was that I couldn't get both to run at the same time
'''
if __name__ ==  "__main__":
	main()

#giant block comment below	
	#multithreading and schlex imports missing
	print "Got into the __main__ where adialog is called"
	filepath = "/home/nao/programs/move.top"
	#line below was commented out
	ad.main()
	args = shlex.split('python adialog_new.py')
	#line below was commented out
	subprocess.Popen(["python", "adialog_new.py"])
	p = subprocess.call(['gnome-terminal', '-x', 'bash', '-c','python adialog.py'])
	#line below was commented out
	Thread(target = func2).start()
	#subprocess.kill()
'''
	
