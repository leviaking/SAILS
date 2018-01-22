#!/usr/bin/env python

##usage example: python annotation_interface.py Core/anno_I03T_Interp-2039.csv
from Tkinter import *
import tkFont, sys, csv, itertools, os
from PIL import ImageTk, Image
from shutil import copyfile


##GLOBAL STUFF

###PRE-PROCESS; this section needs to sort "maybe" ("5") annotations from "yes" ("1") and "no" ("0") annotations. The "maybe" annotations should be written to a separate file, which will then be opened in a slightly modified version of the annotation interface, below.

tempinputfilename=sys.argv[1]  ##inputfilename will be like this: Core/firstpassanno_I29U_Core-2039.csv
# if 'Gramm' in inputfilename:
# 	infilepath='Gramm/'
# elif 'Interp' in inputfilename:
# 	infilepath='Interp/'
# elif 'Core' in inputfilename:
# 	infilepath='Core/'
# elif 'Verif' in inputfilename:
# 	infilepath='Answer/'
# else:
# 	pass
reviewfilename=tempinputfilename.replace('firstpass', 'tempreview')
print 'reviewfilename', reviewfilename
exemptfilename=tempinputfilename.replace('firstpass', 'tempexempt')
print 'exemptfilename', exemptfilename

tempincsv = open(tempinputfilename, 'r')
tempincsvreader=csv.reader(tempincsv, dialect=csv.excel)
tempincsvheadrow=next(tempincsvreader, None)
reviewrows = [tempincsvheadrow]
exemptrows = [tempincsvheadrow]

for tirow in tempincsvreader:
	if tirow[1].strip()=='5': ## '5' indicates a "maybe" annotation
		reviewrows.append(tirow)
	else:
		exemptrows.append(tirow)
tempincsv.close()

reviewfile = open(reviewfilename, 'w')
reviewwriter = csv.writer(reviewfile, dialect=csv.excel)
for rrow in reviewrows:
	reviewwriter.writerow(rrow)
reviewfile.close()

exemptfile = open(exemptfilename, 'w')
exemptwriter = csv.writer(exemptfile, dialect=csv.excel)
for erow in exemptrows:
	exemptwriter.writerow(erow)
exemptfile.close()

originalname=tempinputfilename.split('/')[1]
print 'tempinputfilename', tempinputfilename

inputfilename=str(reviewfilename) ## the original version (below) looks for this variable

### ORIGINAL annotation script (slightly modified)
# inputfilename=inputfilename.split('/')
# inputpath=inputfilename[0]+'/'
# inputfilename=inputfilename[1]
slashsplit=inputfilename.split('/')
#INFFeat2=slashsplit[0]
INF=slashsplit[1]
print 'INF', INF
INFA,INFB=INF.split('-')
print 'INFA, INFB', INFA, INFB
INFNum=INFA[16:18]
print "INFNum", INFNum
INFFeat=INFA[18:] ##e.g., 'TU_Gramm', 'U_Answer', etc.
print "INFFeat", INFFeat
INFFeat2 = INFFeat.split('_')[1] ##e.g., 'Core'
print "INFFeat2", INFFeat2
#INFItem=INFA[19:] ##e.g., 'I06TU', 'I11T'
INFItem=INFA.split('_')[1] ##e.g., 'I06TU', 'I11T'
print "INFItem", INFItem
INFPIN=INFB.split('.')[0] ##e.g., '2039'
# ipath = '../../all_items/figures_300_400/'
ipath = '../../../all_items/figures_200_266/' ##double check this 1/18
FeatNames = ['Gramm', 'Nativ', 'Interp', 'Core', 'Verif', 'Answer']
# if 'Gramm' in inputfilename:
# 	infilepath='Gramm/'
# elif 'Interp' in inputfilename:
# 	infilepath='Interp/'
# elif 'Core' in inputfilename:
# 	infilepath='Core/'
# elif 'Verif' in inputfilename:
# 	infilepath='Answer/'
# else:
# 	pass

## Continue work below this line 1/18

def get_allresponses(csv_in):
	allresponses = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		mheader1 = next(masterreader, None)
		for mrow in masterreader:
			mrow = mrow[0].strip(',')
			print mrow
			allresponses.append(mrow)
	return allresponses

RespStringList = get_allresponses(inputfilename) ##this is a list of responses; 
RespDenominator = len(RespStringList)

header = [INFItem, INFItem+'_'+INFFeat2]
with open(INFFeat2+'/WORKING_'+INF, 'w') as cfile:
	cwriter = csv.writer(cfile, dialect=csv.excel)
	cwriter.writerow(header)

def write_type_csv(resp, anno):
	row=[resp,anno]
	with open(INFFeat2+'/WORKING_'+INF, 'a') as cfile:
		cwriter = csv.writer(cfile, dialect=csv.excel)
		cwriter.writerow(row)
		
def EndOfFile():
	InputName = 'WORKING_'+INF
	FinishedName = InputName[8:]
	FinishedName = FinishedName.replace('tempreview', 'reviewed')
	# try:
	# 	for fn in FeatNames:
	# 		if fn in FinishedName:
	# 			copyfile(InputName, './'+fn+'/'+FinishedName)
	# 		else: pass	
	# except:
	copyfile(INFFeat2+'/'+InputName, INFFeat2+'/'+FinishedName)
	os.remove(INFFeat2+'/'+InputName)
	os.remove(INFFeat2+'/'+INF)

	reviewedname=reviewfilename.replace('tempreview', 'reviewed')
	finalname=reviewedname.replace('reviewed', 'secondpass')
	
	originalfile=open(tempinputfilename, 'r')
	originalreader=csv.reader(originalfile, dialect=csv.excel)
	masterheader=next(originalreader, None)
	originalresponses=[]
	for oline in originalreader:
		originalresponses.append(oline[0])
	originalfile.close()
	
	exemptfile=open(exemptfilename, 'r')
	exemptreader=csv.reader(exemptfile, dialect=csv.excel)
	skipheader=next(exemptreader, None)
	semifinalrows=[]
	for eline in exemptreader:
		semifinalrows.append(eline)
	exemptfile.close()
	os.remove(exemptfilename)
	
	reviewedfile=open(reviewedname, 'r')
	reviewedreader=csv.reader(reviewedfile, dialect=csv.excel)
	skipheader=next(reviewedreader, None)
	for rline in reviewedreader:
		semifinalrows.append(rline)
	reviewedfile.close()
	os.remove(reviewedname)
	
	finalrows=[masterheader]
	for orig in originalresponses:
		for sf in semifinalrows:
			if sf[0].strip()==orig.strip():
				finalrows.append(sf)
	
	finalfile=open(finalname, 'w')
	finalwriter=csv.writer(finalfile, dialect=csv.excel)
	for fr in finalrows:
		finalwriter.writerow(fr)
		
	finalfile.close()






def back_button_edit():
	oldrows=[]
	with open(INFFeat2+'/'+'WORKING_'+INF) as oldfile:
		oldreader = csv.reader(oldfile, dialect=csv.excel)
		for orow in oldreader:
			oldrows.append(orow)
	oldrows=oldrows[:-1]
	with open(INFFeat2+'/'+'TEMP_GO_BACK_'+INF, 'w') as newfile:
		newwriter = csv.writer(newfile, dialect=csv.excel)
		for nrow in oldrows:
			newwriter.writerow(nrow)
	os.remove(INFFeat2+'/'+'WORKING_'+INF)
	os.rename(INFFeat2+'/'+'TEMP_GO_BACK_'+INF, INFFeat2+'/'+'WORKING_'+INF)


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
			  'What is the woman doing?', ## END
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
			  'What is the woman doing?',			  ]
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
	
		# # #RESPONSE LABEL
		self.CurrentRespStringVar = StringVar()
		self.CurrentRespString = Label(self, height=4, width=65, font=tf, textvariable=self.CurrentRespStringVar, anchor='w', wraplength=500, justify='left', bg="bisque")
		self.CurrentRespString.grid(column=0,row=5,columnspan=1, sticky='EW')
		self.CRS = RespStringList[self.CurrentRespNum] ##[0] ###Pay attention to this area (1/17/17)
		self.CRS = self.CRS.rstrip(',')
		self.CurrentRespStringVar.set(self.CRS)

		# # #RESPONSE LABEL
		# # self.CRS = RespStringList[self.CurrentRespNum][0] ###Pay attention to this area (1/17/17)
		# # self.annot = RespStringList[self.CurrentRespNum][1] ###Pay attention ...
		# # if self.annot == '1': ## already annotated "yes" ("1")
		# # #if self.old_annot == '0': ## already annotated "no" ("0")
		# # 	self.SkipButtonVar = StringVar()
		# # 	self.SkipButton = Button(self, font=tf, width=20, highlightbackground="black", text="SKIP", command=self.SkipKey)
		# # 	self.SkipButton.grid(column=0,row=6, columnspan=1, padx=8, pady=8, sticky='W')
		# # 
		# # 	#self.annot=self.old_annot
		# # 	#self.SkipResponse()
		# # 	#write_type_csv(self.CRS, self.annot)
		# # 	#self.CurrentRespNum +=1
		# # 
		# # 	
		# # else:
		# # 	self.CurrentRespStringVar = StringVar()
		# # 	self.CurrentRespString = Label(self, height=4, width=65, font=tf, textvariable=self.CurrentRespStringVar, anchor='w', wraplength=500, justify='left', bg="bisque")
		# # 	self.CurrentRespString.grid(column=0,row=5,columnspan=1, sticky='EW')
		# # 	self.CRS = self.CRS.rstrip(',')
		# # 	self.CurrentRespStringVar.set(self.CRS)
		# # 
		# #YES BUTTON
		# self.YesButtonVar = StringVar()
		# self.YesButton = Button(self, font=tf, width=20, highlightbackground="green", text="Yes", command=self.YesKey)
		# self.YesButton.grid(column=0,row=6, columnspan=1, padx=8, pady=8, sticky='W')
		
		#CHANGE ANNOTATION BUTTON ### CHANGE MAYBE TO YES
		self.ChangeButtonVar = StringVar()
		self.ChangeButton = Button(self, font=tf, width=20, highlightbackground="green", text='''Change "maybe" to "yes"''', command=self.ChangeKey)
		self.ChangeButton.grid(column=0,row=6, columnspan=1, padx=8, pady=8, sticky='W')
	
		#KEEP BUTTON ### CHANGE MAYBE TO NO
		self.KeepButtonVar = StringVar()
		self.KeepButton = Button(self, font=tf, width=20, highlightbackground='red', text='''Change "maybe" to "no"''', command=self.KeepKey)
		self.KeepButton.grid(column=0,row=7, columnspan=1,  padx=8, pady=8, sticky='W')
		
		# #MAYBE BUTTON
		# self.MaybeButtonVar = StringVar()
		# self.MaybeButton = Button(self, width=20, font=tf, text="Not sure", highlightbackground='purple', command=self.MaybeKey)
		# self.MaybeButton.grid(column=0, columnspan=1, row=6,  padx=8, pady=8, sticky='E')
		
		#BACK BUTTON
		self.BackButtonVar = StringVar()
		self.BackButton = Button(self, width=20, font=tf, text="Go back", highlightbackground='powder blue', command=self.BackKey)
		self.BackButton.grid(column=0,row=7, padx=8, pady=8, sticky='E')	

	# def SkipKey(self, event=None):
	# 	#write_type_csv(RespStringList[self.CurrentRespNum][0], self.annot)
	# 	print RespStringList[self.CurrentRespNum][0], RespStringList[self.CurrentRespNum][1]
	# 	write_type_csv(RespStringList[self.CurrentRespNum][0], RespStringList[self.CurrentRespNum][1])
	# 	self.CurrentRespNum +=1
	# 	try:
	# 		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum][0])
	# 		#self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
	# 		#self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
	# 		#self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
	# 		#self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
	# 	except:
	# 		EndOfFile()
			
	def BackKey(self, event=None):
		self.CurrentRespNum -=1
		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])#[0])
		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):\nDo you wish to change the annotation?'
		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		#back_button_reopen(self.CurrentRespNum)
		back_button_edit()
		
	def ChangeKey(self, event=None): ##Change 'maybe' annotation to 'yes'
		self.annot = '1' ## Change '5' to '1'
		#print 'ANNOTATION = '+self.annot
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		try:
			self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])

			self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):\nDo you wish to change the annotation?'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		except:
			EndOfFile()		
		
	def KeepKey(self, event=None): ##Change "maybe" annotation to "no"
		self.annot = '0' ## Change '5' to '0' annotation
		#print 'ANNOTATION = '+self.annot
		write_type_csv(RespStringList[self.CurrentRespNum], self.annot)
		self.CurrentRespNum +=1
		try:
			self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum])
			self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):\nDo you wish to change the annotation?'
			self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
			self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
			self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
		except:
			EndOfFile()
		
	# def MaybeKey(self, event=None):
	# 	self.annot = "5"
	# 	#print 'ANNOTATION ='+self.annot
	# 	write_type_csv(RespStringList[self.CurrentRespNum][0], self.annot)
	# 	self.CurrentRespNum+=1
	# 	try:
	# 		self.CurrentRespStringVar.set(RespStringList[self.CurrentRespNum][0])
	# 		self.counter=' (Response #: '+str(self.CurrentRespNum+1)+'/'+str(RespDenominator)+'):'
	# 		self.AnnotationPrompt = Label(self, font=tf, text=AP+self.counter, width=65, anchor='w', wraplength=500, justify='left')
	# 		self.AnnotationPrompt.grid(column=0, pady=8, row=4, columnspan=1, sticky="W")
	# 		self.AnnotationPromptStringVar.set(self.AnnotationPrompt)
	# 	except:
	# 		EndOfFile()

if __name__ == "__main__":
    root=Tk()
    tf = tkFont.Font(root=root, family='Times New Roman', size=18, weight='bold')
    root.title('PDT Annotation')
    root.geometry('600x800')
    app=App(master=root)
    app.mainloop()
    #root.mainloop()
    root.destroy()

##ABOVE is working... Below this line, we need to combine the reviewed responses/annotations with the exempt responses/annotations, and then sort them according to the original file and write it out as the second pass annotation.

## WORKING HERE, 2018/1/19

##We now have:
##tempinputfilename is 'Core/firstpassanno_I41T_Core-2039.csv'; use this for the original ordering of responses
##exemptfilename is 'Core/tempexemptanno_I41T_Core-2039.csv'
##reviewedanno_I41T_Core-2039.csv
##reviewfilename Core/tempreviewanno_I41T_Core-2039.csv
# reviewedname=reviewfilename.replace('tempreview', 'reviewed')
# finalname=reviewedname.replace('reviewed', 'secondpass')
# 
# originalfile=open(tempinputfilename, 'r')
# originalreader=csv.reader(originalfile, dialect=csv.excel)
# masterheader=next(originalreader, None)
# originalresponses=[]
# for oline in originalreader:
# 	originalresponses.append(oline[0])
# originalfile.close()
# 
# exemptfile=open(exemptfilename, 'r')
# exemptreader=csv.reader(exemptfile, dialect=csv.excel)
# skipheader=next(exemptreader, None)
# semifinalrows=[]
# for eline in exemptreader:
# 	semifinalrows.append(eline)
# exemptfile.close()
# 
# reviewedfile=open(reviewedname, 'r')
# reviewedreader=csv.reader(reviewedfile, dialect=csv.excel)
# skipheader=next(reviewedreader, None)
# for rline in reviewedreader:
# 	semifinalrows.append(rline)
# reviewedfile.close()
# 
# finalrows=[masterheader]
# for orig in originalresponses:
# 	for sf in semifinalrows:
# 		if sf[0].strip()==orig.strip():
# 			finalrows.append(sf)
# 
# finalfile=open(finalname, 'w')
# finalwriter=csv.writer(finalfile, dialect=csv.excel)
# for fr in finalrows:
# 	finalwriter.writerow(fr)
# 	
# finalfile.close()
