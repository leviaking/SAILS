#!/usr/bin/env python

import Tkinter as tk	 # python 2
import tkFont as tkfont  # python 2
import sys, csv, itertools, os
from PIL import ImageTk, Image

class SampleApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.allfileprefixes=['I01TU_Gramm-', 'I01TU_Nativ-', 'I01T_Answer-', 'I01T_Core-', 'I01T_Interp-', 'I01T_Verif-', 'I01U_Answer-', 'I01U_Core-', 'I01U_Interp-', 'I01U_Verif-', 'I02TU_Gramm-', 'I02TU_Nativ-', 'I02T_Answer-', 'I02T_Core-', 'I02T_Interp-', 'I02T_Verif-', 'I02U_Answer-', 'I02U_Core-', 'I02U_Interp-', 'I02U_Verif-', 'I03TU_Gramm-', 'I03TU_Nativ-', 'I03T_Answer-', 'I03T_Core-', 'I03T_Interp-', 'I03T_Verif-', 'I03U_Answer-', 'I03U_Core-', 'I03U_Interp-', 'I03U_Verif-']

		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.currentfolder=os.path.basename(os.path.dirname(os.path.realpath(__file__)))
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		self.geometry('600x800')
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		# for F in (SplashPage, FeatureChoicePage, DeadEnd, GrammFilesPage, NativFilesPage):
		for F in (SplashPage, FeatureChoicePage, DeadEnd, GrammFilesPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("SplashPage")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()


class SplashPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="This is the start page", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, text="Begin annotation (choose a feature)",
							command=lambda: controller.show_frame("FeatureChoicePage"))
		button2 = tk.Button(self, text="Dead end",
							command=lambda: controller.show_frame("DeadEnd"))
		ExitButton = tk.Button(self, text="Exit", command=exit)
		button1.pack()
		button2.pack()
		ExitButton.pack()


class FeatureChoicePage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.allfileprefixes = controller.allfileprefixes
		self.GrammRawFileNames = []
		self.GrammProgNumeratorStringVar = tk.StringVar()
		print "HOLA0: ", self.GrammProgNumeratorStringVar
		self.GrammProgDenominatorStringVar = tk.StringVar()
		# self.NativProgNumeratorStringVar = tk.StringVar()
		# self.NativProgDenominatorStringVar = tk.StringVar()
		# self.NativRawFileNames = []
		self.GrammAnnoFileNames = []
		# self.NativAnnoFileNames = []
		self.ExistingGrammAnnoFileNames = []
		# self.ExistingNativAnnoFileNames = []
		for self.fp in self.allfileprefixes:
			self.rfn=self.fp+controller.currentfolder+'.csv' ##rfn is raw file name (unannotated csv file containing response types)
			self.afn='anno_'+self.rfn
			# print '\t'+self.afn
			if "Gramm" in self.fp:
				self.GrammRawFileNames.append(self.rfn)
				self.GrammAnnoFileNames.append(self.afn)
			# if "Nativ" in self.fp:
			# 	self.NativRawFileNames.append(self.rfn)
			# 	self.NativAnnoFileNames.append(self.afn)
			# self.af=open(self.afn, 'rU')
			# self.af.close()
			try:
				self.af = open(self.afn, 'rU')
				self.af.close()
				print "Found an existing annotation file"
				# print self.afn
				if "Gramm" in self.fp:
					print "It's a Gramm!"
					self.ExistingGrammAnnoFileNames.append(self.afn)
				# if "Nativ" in self.fp:
				# 	self.ExistingNativAnnotatedFileNames.append(self.afn)
				# else: pass
			except:
				print "Nothing to see here..."
				pass
		print "Raw names: ", self.GrammRawFileNames
		# print self.NativRawFileNames
		print "Anno names: ", self.GrammAnnoFileNames
		# print self.NativAnnoFileNames
		print "Existing: ", self.ExistingGrammAnnoFileNames
		# print self.ExistingNativAnnoFileNames

		self.label = tk.Label(self, text="This is the feature choice page", font=controller.title_font)
		self.label.pack(side="top", fill="x", pady=10)
		self.BackButton = tk.Button(self, text="Go back to the start page",
						   command=lambda: controller.show_frame("SplashPage"))
		#self.GrammProgDenominatorStringVar.set(str(len(self.GrammRawFileNames)))
		#print "HOLA: ", self.GrammProgNumeratorStringVar
		print "GrammProgNumerator (declared): ", str(len(self.ExistingGrammAnnoFileNames))
		self.GrammProgNumeratorStringVar.set(str(len(self.ExistingGrammAnnoFileNames[:])))
		#self.GrammProgNumeratorStringVar.set("HELLO")
		print "GrammProgNumeratorStringVar (set): ", str(self.GrammProgNumeratorStringVar)
		# self.NativProgDenominatorStringVar.set(str(len(self.NativRawFileNames)))
		# self.NativProgNumeratorStringVar.set(str(len(self.ExistingNativAnnoFileNames)))
		#print "GrammProgDenominatorStringVar: ", self.GrammProgDenominatorStringVar

		self.GrammButton = tk.Button(self, text=self.GrammProgNumeratorStringVar, command=lambda: controller.show_frame("GrammFilesPage"))
		# GrammButton = tk.Button(self, text="Grammaticality: "+self.GrammProgNumeratorStringVar+'/'+self.GrammProgDenominatorStringVar, command=lambda: controller.show_frame("GrammFilesPage"))
		# NativButton = tk.Button(self, text="Native-likeness: "+self.NativProgNumeratorStringVar+'/'+self.NativProgDenominatorStringVar, command=lambda: controller.show_frame("NativFilesPage"))
		self.BackButton.pack()
		self.GrammButton.pack()
		# NativButton.pack()


class DeadEnd(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="This is a dead end.", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)
		button = tk.Button(self, text="Go back to the start page",
						   command=lambda: controller.show_frame("SplashPage"))
		button.pack()

class GrammFilesPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="Choose a file to annotate: ", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)
		BackButton = tk.Button(self, text="Go back to the start page",
						   command=lambda: controller.show_frame("SplashPage"))
		FileButton = tk.Button(self, text="Gramm File", command=lambda: controller.show_frame("DeadEnd"))
		BackButton.pack()
		FileButton.pack()

# class NativFilesPage(tk.Frame):
# 
# 	def __init__(self, parent, controller):
# 		tk.Frame.__init__(self, parent)
# 		self.controller = controller
# 		label = tk.Label(self, text="Choose a file to annotate: ", font=controller.title_font)
# 		label.pack(side="top", fill="x", pady=10)
# 		BackButton = tk.Button(self, text="Go back to the start page",
# 						   command=lambda: controller.show_frame("SplashPage"))
# 		FileButton = tk.Button(self, text="Nativ File", command=lambda: controller.show_frame("DeadEnd"))
# 		BackButton.pack()
# 		FileButton.pack()

if __name__ == "__main__":
	app = SampleApp()
	app.mainloop()