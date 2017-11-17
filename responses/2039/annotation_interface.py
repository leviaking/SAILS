#!/usr/bin/env python

##usage example: python annotation_interface.py I03T_Interp-2039.csv
from Tkinter import *
import tkFont, sys, csv, itertools, os
from PIL import ImageTk, Image
from shutil import copyfile


##GLOBAL STUFF
inputfilename=sys.argv[1]
INFA,INFB=inputfilename.split('-')
INFNum=INFA[1:3]
INFFeat=INFA[3:] ##e.g., 'TU_Gramm', 'U_Answer', etc.
INFFeat2 = INFFeat.split('_')[1]
INFItem=INFA.split('_')[0] ##e.g., 'I06TU', 'I11T'
INFPIN=INFB.split('.')[0] ##e.g., '2039'
# ipath = '../../all_items/figures_300_400/'
ipath = '../../all_items/figures_200_266/'
FeatNames = ['Gramm', 'Nativ', 'Interp', 'Core', 'Verif', 'Answer']

def get_allresponses(csv_in):
	allresponses = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		mheader1 = next(masterreader, None)
		for mrow in masterreader:
			mrow = mrow[0].strip(',')
			#print mrow
			allresponses.append(mrow)
	return allresponses

RespStringList = get_allresponses(inputfilename)
RespDenominator = len(RespStringList)

header = [INFItem, INFItem+'_'+INFFeat2]
with open('TEMP_'+inputfilename, 'w') as cfile:
	cwriter = csv.writer(cfile, dialect=csv.excel)
	cwriter.writerow(header)

def write_type_csv(resp, anno):
	row=[resp,anno]
	with open('TEMP_'+inputfilename, 'a') as cfile:
		cwriter = csv.writer(cfile, dialect=csv.excel)
		cwriter.writerow(row)
		
def EndOfFile():
	InputName = 'TEMP_'+inputfilename
	FinishedName = 'anno'+InputName[4:]
	try:
		for fn in FeatNames:
			if fn in FinishedName:
				copyfile(InputName, './'+fn+'/'+FinishedName)
			else: pass	
	except:
		copyfile(InputName, FinishedName)
	os.remove(InputName)
		
def back_button_edit():
	oldrows=[]
	with open('TEMP_'+inputfilename) as oldfile:
		oldreader = csv.reader(oldfile, dialect=csv.excel)
		for orow in oldreader:
			oldrows.append(orow)
	oldrows=oldrows[:-1]
	with open('TEMP_GO_BACK_anno_'+inputfilename, 'w') as newfile:
		newwriter = csv.writer(newfile, dialect=csv.excel)
		for nrow in oldrows:
			newwriter.writerow(nrow)
	os.remove('TEMP_'+inputfilename)
	os.rename('TEMP_GO_BACK_anno_'+inputfilename, 'TEMP_'+inputfilename)


FeatDict = {
    'TU_Gramm': 'Does the response below meet the criteria for GRAMMATICALITY?',
    'TU_Nativ': 'Does the response below meet the criteria for NATIVE-LIKENESS?',
    'U_Answer': 'Based on the image and question, does the (untargeted) response meet the criteria for ANSWERHOOD?',
    'T_Answer':'Based on the image and question, does the (targeted) response below meet the criteria for ANSWERHOOD?',
    'U_Core':'Based on the image and question, does the (untargeted) response meet the criteria for CORE EVENT?',
    'T_Core':'Based on the image and question, does the (targeted) response meet the criteria for CORE EVENT?',
    'U_Interp':'Based on the image and question, does the (untargeted) response meet the criteria for INTERPRETABILITY?',
    'T_Interp':'Does the (targeted) response meet the criteria for INTERPRETABILITY?',
    'U_Verif':'Based on the image and question, does the (untargeted) response meet the criteria for VERIFIABILITY?',
    'T_Verif':'Based on the image and question, does the (targeted) response meet the criteria for VERIFIABILITY?'}

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
			  'What is the woman doing?']
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
	
		self.CurrentRespNum = 0
		self.imagenum=INFNum
		self.imagepath=ipath+'I'+self.imagenum+'.jpg'
		
		##QUIT BUTTON
		self.QuitButton = Button(self, font=tf, width=20, highlightbackground="orange", text="Quit", command=self.quit)
		self.QuitButton.grid(column=0,row=0,columnspan=1,sticky='W')
			   
		#QUESTION POINTER
		if INFFeat not in CombinedFeats:
			self.QPointer = Label(self, font=tf, text="Question: ", anchor='w')
			self.QPointer.grid(column=0, row=2, columnspan=1, sticky='W')
		else: pass
			
		#QUESTION LABEL
		if INFFeat not in CombinedFeats:
			self.CurrentQStringVar = StringVar()
			self.CurrentQString = Label(self, height=1, width=65, font=tf, textvariable=self.CurrentQStringVar, anchor='w', wraplength=500, justify='left', bg='azure2')
			self.CurrentQString.grid(column=0, pady=8, row=3,columnspan=1, sticky='EW')
			self.CurrentQStringVar.set(PDTQ)
		else:
			pass
		
		## ANNOTATION PROMPT
		self.AnnotationPromptStringVar = StringVar()
		#print AP
		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)

		# ## IMAGE DISPLAY (working)
		if INFFeat not in CombinedFeats and INFFeat not in NoImgTargFeats and INFFeat not in NoImgUntargFeats:
			self.TempImage = ImageTk.PhotoImage(Image.open(self.imagepath))
			self.CurrentImage = Label(self, image=self.TempImage)
			self.CurrentImage.grid(row=1, column=0, sticky=EW)
		else: pass
	
		#RESPONSE LABEL
		self.CurrentRespStringVar = StringVar()
		self.CurrentRespString = Label(self, height=4, width=65, font=tf, textvariable=self.CurrentRespStringVar,
								   anchor='w', wraplength=500, justify='left', bg="bisque")
		self.CurrentRespString.grid(column=0,row=5,columnspan=1, sticky='EW')
		self.CRS = RespStringList[self.CurrentRespNum]
		self.CRS = self.CRS.rstrip(',')
		self.CurrentRespStringVar.set(self.CRS)
		
		#YES BUTTON
		self.YesButtonVar = StringVar()
		self.YesButton = Button(self, font=tf, width=20, highlightbackground="green", text="Yes", command=self.YesKey)
		self.YesButton.grid(column=0,row=6, columnspan=1, padx=8, pady=8, sticky='W')
	
		#NO BUTTON
		self.NoButtonVar = StringVar()
		self.NoButton = Button(self, font=tf, width=20, highlightbackground='red', text="No", command=self.NoKey)
		self.NoButton.grid(column=0,row=7, columnspan=1,  padx=8, pady=8, sticky='W')
		
		#MAYBE BUTTON
		self.MaybeButtonVar = StringVar()
		self.MaybeButton = Button(self, width=20, font=tf, text="Not sure", highlightbackground='purple', command=self.MaybeKey)
		self.MaybeButton.grid(column=0, columnspan=1, row=6,  padx=8, pady=8, sticky='E')
		
		#BACK BUTTON
		self.BackButtonVar = StringVar()
		self.BackButton = Button(self, width=20, font=tf, text="Go back", highlightbackground='powder blue', command=self.BackKey)
		self.BackButton.grid(column=0,row=7, padx=8, pady=8, sticky='E')	
		
	def BackKey(self, event=None):
		self.CurrentRespNum -=1
		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		#back_button_reopen(self.CurrentRespNum)
		back_button_edit()
		
	def YesKey(self, event=None):
		self.annot = '1'
		#print 'ANNOTATION = '+self.annot
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		try:
			self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])

			self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		except:
			EndOfFile()
			
		
	def NoKey(self, event=None):
		self.annot = '0'
		#print 'ANNOTATION = '+self.annot
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		try:
			self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
			self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		except:
			EndOfFile()
		
	def MaybeKey(self, event=None):
		self.annot = "5"
		#print 'ANNOTATION ='+self.annot
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum+=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		try:
			self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
			self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		except:
			EndOfFile()

if __name__ == "__main__":
    root=Tk()
    tf = tkFont.Font(root=root, family='Times New Roman', size=18, weight='bold')
    root.title('PDT Annotation')
    root.geometry('600x800')
    app=App(master=root)
    app.mainloop()
    #root.mainloop()
    root.destroy()