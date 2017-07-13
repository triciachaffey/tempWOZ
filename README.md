These are the updated files for running the Wizard of Oz experiments.

1. Turn on Nico and wait for it to start.
2. Open terminal. Type: 

	cd ~(path to nri folder)
	
	cd woz
	
	python wizard_gui.py
3. This will open a GUI for the wizard to use during the Wizard of Oz experiments.
4. We implemented interactions and gestures for 21 different nico dialogs.
5. You can also type in a phrase (which doesn't exist in dialog dictionary) in the text entry and pressing the enter key or enter button and Nico will say it. Eg - ‘5 litres of green paint.’

---Notes---

Nico now says and does things at the same time. 
The current version of the code is compatible with running outside of autonomous life and will have Nico return to a crouch position after each movement. 
Because autonomous life is currently disabled, dialog recording will not work. 
This is because adialog_new (the recording piece of the code) relys upon Nico's ability to record which is disabled outside of autonomous mode.
We are currently trying to find a solution to this problem, so any input would be appreciated.
# tempWOZ
