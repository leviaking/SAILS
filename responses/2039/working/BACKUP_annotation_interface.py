#!/usr/bin/env python

##6/9/2017: Functionality to be added: Go back; Review "Maybes"; Resume;

#from Tkinter import *
import Tkinter as tk
import tkFont, sys, csv, itertools, os
from PIL import ImageTk, Image

##GLOBAL STUFF

currentfolder=os.path.basename(os.path.dirname(os.path.realpath(__file__)))
#print currentfolder

allfileprefixes=['I01TU_Gramm-', 'I01TU_Nativ-', 'I01T_Answer-', 'I01T_Core-', 'I01T_Interp-', 'I01T_Verif-', 'I01U_Answer-', 'I01U_Core-', 'I01U_Interp-', 'I01U_Verif-', 'I02TU_Gramm-', 'I02TU_Nativ-', 'I02T_Answer-', 'I02T_Core-', 'I02T_Interp-', 'I02T_Verif-', 'I02U_Answer-', 'I02U_Core-', 'I02U_Interp-', 'I02U_Verif-', 'I03TU_Gramm-', 'I03TU_Nativ-', 'I03T_Answer-', 'I03T_Core-', 'I03T_Interp-', 'I03T_Verif-', 'I03U_Answer-', 'I03U_Core-', 'I03U_Interp-', 'I03U_Verif-', 'I04TU_Gramm-', 'I04TU_Nativ-', 'I04T_Answer-', 'I04T_Core-', 'I04T_Interp-', 'I04T_Verif-', 'I04U_Answer-', 'I04U_Core-', 'I04U_Interp-', 'I04U_Verif-', 'I05TU_Gramm-', 'I05TU_Nativ-', 'I05T_Answer-', 'I05T_Core-', 'I05T_Interp-', 'I05T_Verif-', 'I05U_Answer-', 'I05U_Core-', 'I05U_Interp-', 'I05U_Verif-', 'I06TU_Gramm-', 'I06TU_Nativ-', 'I06T_Answer-', 'I06T_Core-', 'I06T_Interp-', 'I06T_Verif-', 'I06U_Answer-', 'I06U_Core-', 'I06U_Interp-', 'I06U_Verif-', 'I07TU_Gramm-', 'I07TU_Nativ-', 'I07T_Answer-', 'I07T_Core-', 'I07T_Interp-', 'I07T_Verif-', 'I07U_Answer-', 'I07U_Core-', 'I07U_Interp-', 'I07U_Verif-', 'I08TU_Gramm-', 'I08TU_Nativ-', 'I08T_Answer-', 'I08T_Core-', 'I08T_Interp-', 'I08T_Verif-', 'I08U_Answer-', 'I08U_Core-', 'I08U_Interp-', 'I08U_Verif-', 'I09TU_Gramm-', 'I09TU_Nativ-', 'I09T_Answer-', 'I09T_Core-', 'I09T_Interp-', 'I09T_Verif-', 'I09U_Answer-', 'I09U_Core-', 'I09U_Interp-', 'I09U_Verif-', 'I10TU_Gramm-', 'I10TU_Nativ-', 'I10T_Answer-', 'I10T_Core-', 'I10T_Interp-', 'I10T_Verif-', 'I10U_Answer-', 'I10U_Core-', 'I10U_Interp-', 'I10U_Verif-', 'I11TU_Gramm-', 'I11TU_Nativ-', 'I11T_Answer-', 'I11T_Core-', 'I11T_Interp-', 'I11T_Verif-', 'I11U_Answer-', 'I11U_Core-', 'I11U_Interp-', 'I11U_Verif-', 'I12TU_Gramm-', 'I12TU_Nativ-', 'I12T_Answer-', 'I12T_Core-', 'I12T_Interp-', 'I12T_Verif-', 'I12U_Answer-', 'I12U_Core-', 'I12U_Interp-', 'I12U_Verif-', 'I13TU_Gramm-', 'I13TU_Nativ-', 'I13T_Answer-', 'I13T_Core-', 'I13T_Interp-', 'I13T_Verif-', 'I13U_Answer-', 'I13U_Core-', 'I13U_Interp-', 'I13U_Verif-', 'I14TU_Gramm-', 'I14TU_Nativ-', 'I14T_Answer-', 'I14T_Core-', 'I14T_Interp-', 'I14T_Verif-', 'I14U_Answer-', 'I14U_Core-', 'I14U_Interp-', 'I14U_Verif-', 'I15TU_Gramm-', 'I15TU_Nativ-', 'I15T_Answer-', 'I15T_Core-', 'I15T_Interp-', 'I15T_Verif-', 'I15U_Answer-', 'I15U_Core-', 'I15U_Interp-', 'I15U_Verif-', 'I16TU_Gramm-', 'I16TU_Nativ-', 'I16T_Answer-', 'I16T_Core-', 'I16T_Interp-', 'I16T_Verif-', 'I16U_Answer-', 'I16U_Core-', 'I16U_Interp-', 'I16U_Verif-', 'I17TU_Gramm-', 'I17TU_Nativ-', 'I17T_Answer-', 'I17T_Core-', 'I17T_Interp-', 'I17T_Verif-', 'I17U_Answer-', 'I17U_Core-', 'I17U_Interp-', 'I17U_Verif-', 'I18TU_Gramm-', 'I18TU_Nativ-', 'I18T_Answer-', 'I18T_Core-', 'I18T_Interp-', 'I18T_Verif-', 'I18U_Answer-', 'I18U_Core-', 'I18U_Interp-', 'I18U_Verif-', 'I19TU_Gramm-', 'I19TU_Nativ-', 'I19T_Answer-', 'I19T_Core-', 'I19T_Interp-', 'I19T_Verif-', 'I19U_Answer-', 'I19U_Core-', 'I19U_Interp-', 'I19U_Verif-', 'I20TU_Gramm-', 'I20TU_Nativ-', 'I20T_Answer-', 'I20T_Core-', 'I20T_Interp-', 'I20T_Verif-', 'I20U_Answer-', 'I20U_Core-', 'I20U_Interp-', 'I20U_Verif-', 'I21TU_Gramm-', 'I21TU_Nativ-', 'I21T_Answer-', 'I21T_Core-', 'I21T_Interp-', 'I21T_Verif-', 'I21U_Answer-', 'I21U_Core-', 'I21U_Interp-', 'I21U_Verif-', 'I22TU_Gramm-', 'I22TU_Nativ-', 'I22T_Answer-', 'I22T_Core-', 'I22T_Interp-', 'I22T_Verif-', 'I22U_Answer-', 'I22U_Core-', 'I22U_Interp-', 'I22U_Verif-', 'I23TU_Gramm-', 'I23TU_Nativ-', 'I23T_Answer-', 'I23T_Core-', 'I23T_Interp-', 'I23T_Verif-', 'I23U_Answer-', 'I23U_Core-', 'I23U_Interp-', 'I23U_Verif-', 'I24TU_Gramm-', 'I24TU_Nativ-', 'I24T_Answer-', 'I24T_Core-', 'I24T_Interp-', 'I24T_Verif-', 'I24U_Answer-', 'I24U_Core-', 'I24U_Interp-', 'I24U_Verif-', 'I25TU_Gramm-', 'I25TU_Nativ-', 'I25T_Answer-', 'I25T_Core-', 'I25T_Interp-', 'I25T_Verif-', 'I25U_Answer-', 'I25U_Core-', 'I25U_Interp-', 'I25U_Verif-', 'I26TU_Gramm-', 'I26TU_Nativ-', 'I26T_Answer-', 'I26T_Core-', 'I26T_Interp-', 'I26T_Verif-', 'I26U_Answer-', 'I26U_Core-', 'I26U_Interp-', 'I26U_Verif-', 'I27TU_Gramm-', 'I27TU_Nativ-', 'I27T_Answer-', 'I27T_Core-', 'I27T_Interp-', 'I27T_Verif-', 'I27U_Answer-', 'I27U_Core-', 'I27U_Interp-', 'I27U_Verif-', 'I28TU_Gramm-', 'I28TU_Nativ-', 'I28T_Answer-', 'I28T_Core-', 'I28T_Interp-', 'I28T_Verif-', 'I28U_Answer-', 'I28U_Core-', 'I28U_Interp-', 'I28U_Verif-', 'I29TU_Gramm-', 'I29TU_Nativ-', 'I29T_Answer-', 'I29T_Core-', 'I29T_Interp-', 'I29T_Verif-', 'I29U_Answer-', 'I29U_Core-', 'I29U_Interp-', 'I29U_Verif-', 'I30TU_Gramm-', 'I30TU_Nativ-', 'I30T_Answer-', 'I30T_Core-', 'I30T_Interp-', 'I30T_Verif-', 'I30U_Answer-', 'I30U_Core-', 'I30U_Interp-', 'I30U_Verif-']
rawfilenames=[]
for afp in allfileprefixes:
	rawfilenames.append(afp+currentfolder+'.csv')

annofilenames=[]

inputfilename=sys.argv[1]
INFA,INFB=inputfilename.split('-')
INFNum=INFA[1:3] 
INFFeat=INFA[3:] ##e.g., 'TU_Gramm', 'U_Answer', etc.
INFFeat2 = INFFeat.split('_')[1]
INFItem=INFA.split('_')[0] ##e.g., 'I06TU', 'I11T'
INFPIN=INFB.split('.')[0] ##e.g., '2039'
ipath = '../../../all_items/figures_300_400/'

def initialize_currentresponsenum(inputfilename):
	annorows=[]
	try:
		annofile=open('anno_'+inputfilename, 'rU')
		annoreader = csv.reader(annofile, dialect=csv.excel)
		#aheader1 = next(annoreader, None)
		for arow in annoreader:
			arow = arow[0].strip(',')
			annorows.append(arow)
		annofile.close()
		resumenum=len(annorows)
	except:
		resumenum=0
		annofile='NONE'
	if not annorows:
		header = [INFItem, INFItem+'_'+INFFeat2]
		cf=open('anno_'+inputfilename, 'w')
		# with open('anno_'+inputfilename, 'w') as cfile:
		cfwriter = csv.writer(cf, dialect=csv.excel)
		cfwriter.writerow(header)
		cf.close()
	# if annofile=='NONE':
	# 	print 'No File'
	# else:
	# 	print annofile
	return resumenum

resumenum = initialize_currentresponsenum(inputfilename)

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

# def get_cwriter(rn): ##resumenum
# 	if rn == '0':
# 		header = [INFItem, INFItem+'_'+INFFeat2]
# 		cf=open('anno_'+inputfilename, 'w')
# 		# with open('anno_'+inputfilename, 'w') as cfile:
# 		cwriter = csv.writer(cf, dialect=csv.excel)
# 		cwriter.writerow(header)
# 	else:
# 		cf=open('anno_'+inputfilename, 'a')
# 		cwriter = csv.writer(cf, dialect=csv.excel)
# 	return cwriter

# cwriter = get_cwriter(resumenum)

def write_type_csv(resp, anno):
	with open('anno_'+inputfilename, 'a') as cfile:
	# cf=open('anno_'+inputfilename, 'a')
		cwriter = csv.writer(cfile, dialect=csv.excel)
		row=[resp,anno]
		cwriter.writerow(row)
	# with open('anno_'+inputfilename, 'a') as cfile:
	# 	cwriter = csv.writer(cfile, dialect=csv.excel)
	# 	cwriter.writerow(row)
		
def back_button_edit():
	oldrows=[]
	with open('anno_'+inputfilename) as oldfile:
		oldreader = csv.reader(oldfile, dialect=csv.excel)
		for orow in oldreader:
			oldrows.append(orow)
	oldrows=oldrows[:-1]
	with open('TEMP_GO_BACK_anno_'+inputfilename, 'w') as newfile:
		newwriter = csv.writer(newfile, dialect=csv.excel)
		for nrow in oldrows:
			newwriter.writerow(nrow)
	os.remove('anno_'+inputfilename)
	os.rename('TEMP_GO_BACK_anno_'+inputfilename, 'anno_'+inputfilename)


FeatDict = {
    'TU_Gramm': 'Does the response below meet the criteria for GRAMMATICALITY?',
    'TU_Nativ': 'Does the response below meet the criteria for NATIVE-LIKENESS?',
    'U_Answer': 'Based on the image and question, does the (untargeted) response meet the criteria for ANSWERHOOD?',
    'T_Answer':'Based on the image and question, does the (targeted) response below meet the criteria for ANSWERHOOD?',
    'U_Core':'Based on the image and question, does the (untargeted) response meet the criteria for CORE EVENT?',
    'T_Core':'Based on the image and question, does the (targeted) response meet the criteria for CORE EVENT?',
    'U_Interp':'Based on the image and question, does the (untargeted) response meet the criteria for INTERPRETABILITY?',
    'T_Interp':'Based on the image and question, does the (targeted) response meet the criteria for INTERPRETABILITY?',
    'U_Verif':'Based on the image and question, does the (untargeted) response meet the criteria for VERIFIABILITY?',
    'T_Verif':'Based on the image and question, does the (targeted) response meet the criteria for VERIFIABILITY?'}

TargFeats = ['T_Answer', 'T_Core', 'T_Interp', 'T_Verif']
UntargFeats = ['U_Answer', 'U_Core', 'U_Interp', 'U_Verif']
CombinedFeats = ['TU_Gramm', 'TU_Nativ']
UntargetedQ = 'What is happening?'
TargetedQs = ['What is the boy doing?', 'What is the boy doing?', 'What is the man doing?', 'What is the boy doing?', 'What is the teacher doing?', 'What is the boy doing?', 'What is the bird doing?', 'What is the waiter doing?', 'What is the girl doing?', 'What is the baby doing?', 'What is the boy doing?', 'What is the woman doing?', 'What is the man doing?', 'What is the man doing?', 'What is the man doing?', 'What is the frog doing?', 'What is the man doing?', 'What is the girl doing?', 'What is the man doing?', 'What is the woman doing?', 'What is the girl doing?', 'What is the boy doing?', 'What is the woman doing?', 'What is the doctor doing?', 'What is the boy doing?', 'What is the dog doing?', 'What is the man doing?', 'What is the girls doing?', 'What is the man doing?', 'What is the woman doing?', 'What is the woman doing?']
CombinedQ = ''

AP = FeatDict[INFFeat]

if INFFeat in TargFeats:
    PDTQ = TargetedQs[int(INFNum)-1]
if INFFeat in UntargFeats:
    PDTQ = UntargetedQ
if INFFeat in CombinedFeats:
    PDTQ = CombinedQ

class MainApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title_font = tkFont.Font(family='Helvetica', size=18, weight='bold')
		# self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		for F in (LaunchFrame, AnnotationFrame):
			page_name = F.__name__
			#frame = F(parent=container, controller=self)
			frame = F(parent=container, master=self)
			self.frames[page_name] = frame
			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame("StartPage")
	
	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()


class LaunchFrame(tk.Frame):
	# def __init__(self,master):
	# 	Frame.__init__(self,master)
	def __init__(self,master,controller):
		Frame.__init__(self,master, controller)
		self.pack()
		self.LaunchStatus=0
		self.rawfilenames=[]
		self.GrammAnnotated=0
		self.NativAnnotated=0
		self.InterpAnnotated=0
		self.CoreAnnotated=0
		self.VerifAnnotated=0
		self.AnswerAnnotated=0
		# self.junk = 0
		# while self.junk < 5:
		# 	if self.LaunchStatus==1:
		# 		self.FileSelectionApp=FileSelectionFrame(master=root)
		# 		self.FileSelectionApp
		# 		self.FileSelectionApp.mainloop()

		for self.fp in allfileprefixes:
			self.rfn=self.fp+currentfolder+'.csv' ##rfn is raw file name (unannotated csv file containing response types)
			self.afn='anno_'+self.rfn
			# self.rfnlines=0
			# self.afnlines=0
			try:
				self.af = open(self.afn, 'rU')
				self.af.close()
			except:
				self.af = 'NONE'
			if 'Gramm' in self.fp and self.af != 'NONE':
				self.GrammAnnotated+=1
			if 'Nativ' in self.fp and self.af != 'NONE':
				self.NativAnnotated+=1
			if 'Interp' in self.fp and self.af != 'NONE':
				self.InterpAnnotated+=1				
			if 'Core' in self.fp and self.af != 'NONE':
				self.CoreAnnotated+=1
			if 'Verif' in self.fp and self.af != 'NONE':
				self.VerifAnnotated+=1
			if 'Answer' in self.fp and self.af != 'NONE':
				self.AnswerAnnotated+=1
		self.GrammProg = str(self.GrammAnnotated)+'/30'
		self.NativProg = str(self.NativAnnotated)+'/30'
		self.InterpProg= str(self.InterpAnnotated)+'/60'
		self.CoreProg = str(self.CoreAnnotated)+'/60'
		self.VerifProg = str(self.VerifAnnotated)+'/60'
		self.AnswerProg = str(self.AnswerAnnotated)+'/60'

		##QUIT BUTTON
		self.QuitButton = Button(self, font=tf, width=20, highlightbackground="orange", text="Quit", wraplength=500, command=self.quit)
		self.QuitButton.grid(column=0,row=0,columnspan=1,padx=8, pady=8, sticky='W')
		
		## SELECTION PROMPT
		#self.SelectionPromptStringVar = StringVar()
		self.AnnotationPrompt = Label(self, font=tf, text='Please choose a feature to annotate. The progress displayed here is an approximation -- some features that appear complete may be incomplete', width=65, wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=2, columnspan=1, sticky="EW")
		#self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		
		#GRAMM BUTTON
		self.GrammButtonVar = StringVar()
		self.GrammButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Grammaticality: "+self.GrammProg, command=self.GrammKey)
		self.GrammButton.grid(column=0,row=3, padx=8, pady=8, sticky='W')
		
		#NATIV BUTTON
		self.NativButtonVar = StringVar()
		self.NativButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Native-likeness: "+self.NativProg, command=self.NativKey)
		self.NativButton.grid(column=0,row=4, columnspan=1, padx=8, pady=8, sticky='W')

		#INTERP BUTTON
		self.InterpButtonVar = StringVar()
		self.InterpButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Interpretability: "+self.InterpProg, command=self.InterpKey)
		self.InterpButton.grid(column=0,row=5, columnspan=1, padx=8, pady=8, sticky='W')
		
		#CORE BUTTON
		self.CoreButtonVar = StringVar()
		self.CoreButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Core Event: "+self.CoreProg, command=self.CoreKey)
		self.CoreButton.grid(column=0, row=3, padx=8, pady=8, sticky='E')
		
		#VERIF BUTTON
		self.VerifButtonVar = StringVar()
		self.VerifButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Verifiability: "+self.VerifProg, command=self.VerifKey)
		self.VerifButton.grid(column=0,row=4, columnspan=1, padx=8, pady=8, sticky='E')
		
		#ANSWERHOOD BUTTON
		self.AnswerButtonVar = StringVar()
		self.AnswerButton = Button(self, font=tf, width=20, highlightbackground="blue", text="Answerhood: "+self.AnswerProg, command=self.AnswerKey)
		self.AnswerButton.grid(column=0,row=5, columnspan=1, padx=8, pady=8, sticky='E')

	def GrammKey(self, event=None):
		self.Feature='Gramm'
		self.GrammAnnoList=[]
		self.GrammAnnoDict={}
		for self.fp in allfileprefixes:
			if "Gramm" not in self.fp:
				pass
			else: #"Gramm" in self.fp:
				self.rfn=self.fp+currentfolder+'.csv' ##rfn is raw file name (unannotated csv file containing response types)
				self.afn='anno_'+self.rfn
				self.rflines=0
				self.aflines=0
				try:
					self.rf = open(self.rfn, 'rU')
					self.rfreader=csv.reader(self.rf, dialect=csv.excel)
					for self.rfrow in self.rfreader:
						self.rflines +=1
					self.rf.close()
				except:
					pass
				try:
					self.af = open(self.afn, 'rU')
					self.afreader = csv.reader(self.af, dialect=csv.excel)
					for self.afrow in self.afreader:
						self.aflines+=1
					self.af.close()
				except:
					pass
			print self.fp+' : '+str(self.aflines)+'/'+str(self.rflines)
			self.GrammAnnoList.append(self.fp)
			self.GrammAnnoDict[self.fp]=self.fp[:-1]+': '+str(self.aflines)+'/'+str(self.rflines)
		self.GrammAnnoList.sort()
		# self.LaunchStatus=1
		return self.Feature, self.GrammAnnoList, self.GrammAnnoDict
		# FileSelectionApp=FileSelectionFrame(master=root)
		# FileSelectionApp.mainloop()
		# LaunchApp.destroy()
		



	def NativKey(self, event=None):
		pass
	def InterpKey(self, event=None):
		pass
	def CoreKey(self, event=None):
		pass
	def VerifKey(self, event=None):
		pass
	def AnswerKey(self, event=None):
		pass

class FileSelectionFrame(tk.Frame):
	def __init__(self,master):
		Frame.__init__(self,master)
		self.pack()
		print LaunchApp.GrammAnnoList


class AnnotationFrame(tk.Frame):
	def __init__(self,master):
		Frame.__init__(self,master)
		self.pack()
		#self.createWidgets()
	
		self.CurrentRespNum = resumenum
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
		if INFFeat not in CombinedFeats:
			self.TempImage = ImageTk.PhotoImage(Image.open(self.imagepath))
			self.CurrentImage = Label(self, image=self.TempImage)
			self.CurrentImage.grid(row=1, column=0, sticky=EW)
		else: pass
	
		#RESPONSE LABEL
		self.CurrentRespStringVar = StringVar()
		self.CurrentRespString = Label(self, height=4, width=65, font=tf, textvariable=self.CurrentRespStringVar,
								   anchor='w', wraplength=500, justify='left', bg="bisque")
		self.CurrentRespString.grid(column=0,row=5,columnspan=1, sticky='EW')
		try:
			self.CRS = RespStringList[self.CurrentRespNum]
		except:
			print "This annotation file appears to be complete. You can review and annotate responses marked 'maybe', or you can close this window and annotate a different file.\n"
			self.quit
			quit()
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
	
	# def InitializeCurrentRespNum(self, event=None):
	# 	pass
		
	
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
		#write_type_csv(cwriter, RespStringList[self.CurrentRespNum], self.annot)
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])

		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		
	def NoKey(self, event=None):
		self.annot = '0'
		#print 'ANNOTATION = '+self.annot
		#write_type_csv(cwriter, RespStringList[self.CurrentRespNum], self.annot)
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
		
		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		
	def MaybeKey(self, event=None):
		self.annot = "5"
		#print 'ANNOTATION ='+self.annot
		#write_type_csv(cwriter, RespStringList[self.CurrentRespNum], self.annot)
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum+=1
		#self.CRS = RespStringList[self.CurrentRespNum]
		#self.CRS = self.CRS.rstrip(',')
		#self.CurrentRespStringVar.set(self.CRS)
		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# if __name__ == "__main__":
# 	root=Tk()
# 	tf = tkFont.Font(root=root, family='Times New Roman', size=18, weight='bold')
# 	root.title('PDT Annotation')
# 	root.geometry('600x800')
# 	LaunchApp=LaunchFrame(master=root)
# 	LaunchApp.mainloop()
# 	# AnnotationApp=AnnotationFrame(master=root)
# 	# #print AnnotationApp.CurrentRespNum
# 	# AnnotationApp.mainloop()
# 	# #root.mainloop()
# 	# root.destroy()