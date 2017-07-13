import wizard_gui as wozGUI
import adialog_new as ad
from threading import Thread

'''
I was looking at this page on threading: https://stackoverflow.com/questions/23100704/running-infinite-loops-using-threads-in-python/23102874#23102874
'''

class callGUI(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
		self.start()
	def run(self):
		while True:
			wozGUI.main()

class callDialog(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
		self.start()
	def run(self):
		while True:
			ad.main()


callGUI()
callDialog()
while True:
	pass
