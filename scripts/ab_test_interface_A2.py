#!/usr/bin/env python

##usage example: python ab_test_interface_A2.py
from Tkinter import *
import tkFont, sys, csv, itertools, os
from PIL import ImageTk, Image
from shutil import copyfile


##GLOBAL STUFF
# # inputfilename=sys.argv[1]
inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs_for_A2.csv'
# # INFA,INFB=inputfilename.split('-')
# # INFNum=INFA[1:3]
INFNum = '31'
# # INFFeat=INFA[3:] ##e.g., 'TU_Gramm', 'U_Answer', etc.
INFFeat = 'T_Interp'
# # INFFeat2 = INFFeat.split('_')[1]
# # INFItem=INFA.split('_')[0] ##e.g., 'I06TU', 'I11T'
# # INFPIN=INFB.split('.')[0] ##e.g., '2039'
ipath = '/Users/leviking/Documents/dissertation/SAILS/all_items/figures_200_266/'
FeatNames = ['Gramm', 'Nativ', 'Interp', 'Core', 'Verif', 'Answer']

def get_all_input_rows(csv_in):
	allrows = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		mheader = next(masterreader, None)
		for mrow in masterreader:
			# mrow = mrow[0].strip(',')
			allrows.append(mrow)
	return allrows

def get_responses_from_rows(myrows):
	resps = []
	for mr in myrows:
		resps.append(mr[13])
	return resps


response_rows = get_all_input_rows(inputfilename)
header = ['Response', 'Better', 'Worse', 'Same']
RespStringList = get_responses_from_rows(response_rows)
RespDenominator = len(RespStringList)/2  ## /2 to get number of pairs

# # header = [INFItem, INFItem+'_'+INFFeat2]
with open(inputfilename.split('.csv')[0]+'-TOYY-A2.csv', 'w') as cfile:
	cwriter = csv.writer(cfile, dialect=csv.excel)
	cwriter.writerow(header)

def write_type_csv(resp, win, lose, tie):
	row=[resp,win, lose, tie]
	with open(inputfilename.split('.csv')[0]+'-TOYY-A2.csv', 'a') as cfile:
		cwriter = csv.writer(cfile, dialect=csv.excel)
		cwriter.writerow(row)
		
def EndOfFile():
	InputName = inputfilename.split('.csv')[0]+'-TOYY-A2.csv'
	FinishedName = 'anno'+InputName[4:]
	try:
		for fn in FeatNames:
			if fn in FinishedName:
				copyfile(InputName, './'+fn+'/'+FinishedName)
			else: pass	
	except:
		copyfile(InputName, FinishedName)
	# # os.remove(InputName)
		
def back_button_edit():
	oldrows=[]
	with open(inputfilename.split('.csv')[0]+'-TOYY-A2.csv') as oldfile:
		oldreader = csv.reader(oldfile, dialect=csv.excel)
		for orow in oldreader:
			oldrows.append(orow)
	oldrows=oldrows[:-1]
	with open('TOYY-A2_GO_BACK_anno_'+inputfilename, 'w') as newfile:
		newwriter = csv.writer(newfile, dialect=csv.excel)
		for nrow in oldrows:
			newwriter.writerow(nrow)
	os.remove(inputfilename.split('.csv')[0]+'-TOYY-A2.csv')
	os.rename('TOYY-A2_GO_BACK_anno_'+inputfilename, inputfilename.split('.csv')[0]+'-TOYY-A2.csv')

FeatDict = {
    'TU_Gramm': 'Which is the best response for this task?',
    'TU_Nativ': 'Which is the best response for this task?',
    'U_Answer': 'Which is the best response for this task?',
    'T_Answer':'Which is the best response for this task?',
    'U_Core':'Which is the best response for this task?',
    'T_Core':'Which is the best response for this task?',
    'U_Interp':'Which is the best response for this task?',
    'T_Interp':'Which is the best response for this task?',
    'U_Verif':'Which is the best response for this task?',
    'T_Verif':'Which is the best response for this task?',}

TargFeats = ['T_Answer', 'T_Core', 'T_Interp', 'T_Verif']
NoImgTargFeats = ['T_Interp']
UntargFeats = ['U_Answer', 'U_Core', 'U_Interp', 'U_Verif']
NoImgUntargFeats = ['U_Answer', 'U_Interp']
CombinedFeats = ['TU_Gramm', 'TU_Nativ']
UntargetedQ = 'What is happening?'
TargetedQs = ['What is the boy doing?',
			  'What is the boy doing?',
			  'What is the man doing?',
			  'What is the boy doing?',
			  'What is the teacher doing?',
			  'What is the boy doing?',
			  'What is the bird doing?',
			  'What is the waiter doing?',
			  'What is the girl doing?',
			  'What is the baby doing?',
			  'What is the boy doing?',
			  'What is the woman doing?',
			  'What is the man doing?',
			  'What is the man doing?',
			  'What is the man doing?',
			  'What is the frog doing?',
			  'What is the girl doing?',
			  'What is the man doing?',
			  'What is the woman doing?',
			  'What is the girl doing?',
			  'What is the boy doing?',
			  'What is the woman doing?',
			  'What is the doctor doing?',
			  'What is the boy doing?',
			  'What is the dog doing?',
			  'What is the man doing?',
			  'What is the girl doing?',
			  'What is the man doing?',
			  'What is the woman doing?',
			  'What is the woman doing?'
			  'What is Randy doing?',
			  'What is Randy doing?']
CombinedQ = ''

AP = FeatDict[INFFeat]

if INFFeat in TargFeats:
    PDTQ = TargetedQs[int(INFNum)-1]
if INFFeat in UntargFeats:
    PDTQ = UntargetedQ
if INFFeat in CombinedFeats:
    PDTQ = CombinedQ

class App(Frame):
	def __init__(self,master):
		Frame.__init__(self,master)
		self.pack()
		#self.createWidgets()
	
		self.LeftRespNum = 0
		self.RightRespNum = 1
		self.imagenum=INFNum
		self.imagepath=ipath+'I'+self.imagenum+'.jpg'
		
		##QUIT BUTTON
		self.QuitButton = Button(self, font=tf, width=20, highlightbackground="orange", text="Quit", command=self.quit)
		self.QuitButton.grid(column=0,row=0,columnspan=1,sticky='W')
			
		#QUESTION POINTER
		# if INFFeat not in CombinedFeats:
		# 	self.QPointer = Label(self, font=tf, text="Question: ", anchor='w')
		# 	self.QPointer.grid(column=0, row=2, columnspan=1, sticky='W')
		# else: pass
			
		# # #QUESTION LABEL
		# # if INFFeat not in CombinedFeats:
		# # 	self.LeftQStringVar = StringVar()
		# # 	self.LeftQString = Label(self, height=1, width=65, font=tf, textvariable=self.LeftQStringVar, anchor='w', wraplength=500, justify='left', bg='azure2')
		# # 	self.LeftQString.grid(column=0, pady=8, row=3,columnspan=1, sticky='EW')
		# # 	self.LeftQStringVar.set(PDTQ)
		# # else:
		# # 	pass
		
		## ANNOTATION PROMPT
		self.AnnotationPromptStringVar = StringVar()
		#print AP
		self.counter=' (Pair #: '+str(self.RightRespNum)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)

		# # ## IMAGE DISPLAY
		# if INFFeat not in CombinedFeats and INFFeat not in NoImgTargFeats and INFFeat not in NoImgUntargFeats:
		# 	self.TOYY-A2Image = ImageTk.PhotoImage(Image.open(self.imagepath))
		# 	self.LeftImage = Label(self, image=self.TOYY-A2Image)
		# 	self.LeftImage.grid(row=1, column=0, sticky=EW)
		# else: pass

		#RESPONSE LABEL
		self.LeftRespStringVar = StringVar()
		# self.LeftRespString = Label(self, height=4, width=65, font=tf, textvariable=self.LeftRespStringVar,
		# 						   anchor='w', wraplength=500, justify='left', bg="PaleTurquoise1")
		# self.LeftRespString.grid(column=0,row=5,columnspan=1, sticky='EW')
		self.LeftCRS = RespStringList[self.LeftRespNum]
		self.LeftCRS = self.LeftCRS.rstrip(',')
		#LEFT BUTTON
		self.LeftButtonVar = StringVar()
		self.LeftButton = Button(self, height=4, font=tf, textvariable=self.LeftRespStringVar,
								anchor='w',justify=LEFT, highlightbackground="turquoise1", command=self.LeftKey)
		self.LeftButton.grid(column=0,row=5,columnspan=1, sticky='EW', padx=20)
		self.LeftRespStringVar.set(self.LeftCRS)
		
		self.RightRespStringVar = StringVar()
		# self.RightRespString = Label(self, height=4, width=65, font=tf, textvariable=self.RightRespStringVar,
		# 						   anchor='e', wraplength=500, justify='left', bg="LightGoldenrod1")
		# self.RightRespString.grid(column=0,row=6,columnspan=1, sticky='EW')
		self.RightCRS = RespStringList[self.RightRespNum]
		self.RightCRS = self.RightCRS.rstrip(',')
		#Right BUTTON
		self.RightButtonVar = StringVar()
		self.RightButton = Button(self, height=4, font=tf, textvariable=self.RightRespStringVar,
								anchor='e', justify=LEFT, highlightbackground="LightGoldenrod1", command=self.RightKey)
		self.RightButton.grid(column=0,row=6,columnspan=1, sticky='EW', padx=20)
		self.RightRespStringVar.set(self.RightCRS)
		
		#MAYBE BUTTON
		self.MaybeButtonVar = StringVar()
		self.MaybeButton = Button(self, width=20, font=tf, text="Same/Unsure", highlightbackground='pale green', command=self.MaybeKey)
		self.MaybeButton.grid(column=0, columnspan=1, row=8,  padx=170, pady=8, sticky='EW')
		
	# 	#BACK BUTTON
	# 	self.BackButtonVar = StringVar()
	# 	self.BackButton = Button(self, width=20, font=tf, text="Go back", highlightbackground='powder blue', command=self.BackKey)
	# 	self.BackButton.grid(column=0,row=8, padx=8, pady=8, sticky='E')	
	# 	
	# def BackKey(self, event=None):
	# 	self.LeftRespNum -=2
	# 	self.RightRespNum -=2
	# 	self.LeftRespStringVar.set(RespStringList[self.LeftRespNum])
	# 	self.RightRespStringVar.set(RespStringList[self.RightRespNum])
	# 	self.counter=' (Pair #: '+str(self.LeftRespNum+1)+'/'+str(RespDenominator)+'):'
	# 	self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
	# 	self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
	# 	self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
	# 	back_button_edit()
	 	
	def LeftKey(self, event=None):
		self.LWin = '1'
		self.LLose = '0'
		self.LTie = '0'
		self.RWin = '0'
		self.RLose = '1'
		self.RTie = '0'
		write_type_csv(RespStringList[self.LeftRespNum], self.LWin, self.LLose, self.LTie)
		write_type_csv(RespStringList[self.RightRespNum], self.RWin, self.RLose, self.RTie)
		self.LeftRespNum +=2
		self.RightRespNum +=2
		try:
			self.LeftRespStringVar.set(RespStringList[self.LeftRespNum])
			self.counter=' (Pair #: '+str((self.RightRespNum+1)/2)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
			#
			self.RightRespStringVar.set(RespStringList[self.RightRespNum])
		except:
			EndOfFile()
			
		
	def RightKey(self, event=None):
		self.LWin = '0'
		self.LLose = '1'
		self.LTie = '0'
		self.RWin = '1'
		self.RLose = '0'
		self.RTie = '0'
		write_type_csv(RespStringList[self.LeftRespNum], self.LWin, self.LLose, self.LTie)
		write_type_csv(RespStringList[self.RightRespNum], self.RWin, self.RLose, self.RTie)
		self.LeftRespNum +=2
		self.RightRespNum +=2
		try:
			self.LeftRespStringVar.set(RespStringList[self.LeftRespNum])
			self.counter=' (Pair #: '+str((self.RightRespNum+1)/2)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
			#
			self.RightRespStringVar.set(RespStringList[self.RightRespNum])
		except:
			EndOfFile()
		
	def MaybeKey(self, event=None):
		self.LWin = '0'
		self.LLose = '0'
		self.LTie = '1'
		self.RWin = '0'
		self.RLose = '0'
		self.RTie = '1'
		write_type_csv(RespStringList[self.LeftRespNum], self.LWin, self.LLose, self.LTie)
		write_type_csv(RespStringList[self.RightRespNum], self.RWin, self.RLose, self.RTie)
		self.LeftRespNum+=2
		self.RightRespNum +=2
		try:
			self.LeftRespStringVar.set(RespStringList[self.LeftRespNum])
			self.counter=' (Pair #: '+str((self.RightRespNum+1)/2)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
			#
			self.RightRespStringVar.set(RespStringList[self.RightRespNum])
		except:
			EndOfFile()

if __name__ == "__main__":
    root=Tk()
    tf = tkFont.Font(root=root, family='Times New Roman', size=18, weight='bold')
    root.title('PDT Annotation')
    root.geometry('600x800')
    app=App(master=root)
    app.mainloop()
    root.destroy()