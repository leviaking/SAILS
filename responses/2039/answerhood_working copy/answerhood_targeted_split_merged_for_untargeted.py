#!/usr/bin/env python

##STOP! WARNING! This script is wrong -- it generates files for untargeted annotation which are not the right files. This generates untargeted files that are entirely derived from the targeted files. Instead, I should simply use the files output here as *TEMP-YES.csv. These are targeted responses that should be annotated in the same way if they occur in the untargeted responses. I now have a script called applyTargetedAnnoToUntargeted.py that will take the *TEMP-YES.csv files as input and apply the annotations to untargeted responses.

###############

##This script takes the annotated answerhood targeted file, which is a merged file of the manually annotated targeted responses and the automatically rejected targeted responses. It splits the file into A & B: all A responses are annotated 'yes' for Untargeted (carried over from Targeted); all B responses need to be manually annotated. Basically, ALL responses with targeted annotation 'no' need to be manually annotated; additionally, SOME with targeted annotation 'yes' need to be manually annotated. These will be responses that:
##	omit the subject (because it's understood from the targeted question, but not the untargeted question), OR
##	consist solely of a noun activity that can be done; e.g., Q: What is the girl doing? A: Origami.
##Thus we need to read in each line of the annotated targeted merged file. For each line, we check:
##	if annotation == '1': ## aka 'yes'
##		if one of SubjVariants in Response: ##if a subject (a string) in the list of the targeted subject and accepted variants is found in the response, then we know the response is almost certainly a complete sentence; since we already know from the annotation it was accepted for targeted items, we now know it can be automatically annotated 'yes' for untargeted also.
##			AutoYesList.append(response)
##		else:
##			ManualAnnotateList.append(response)
##	else: ## i.e., if annotation == '0' or annotation == '5' (i.e., targeted annotation is yes or maybe)
##		ManualAnnotateList.append(response)


import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

subjects = [
	['the boy', 'he ', "he's",], #1
	['the boy', 'he ', "he's",],
	['the man', 'he ', "he's",],
	['the boy', 'he ', "he's",],
	['the teacher', 'she ', "she's"], #5
	['the boy', 'he ', "he's",],
	['the bird', 'it ', "it's", 'he ', "he's", 'she ', "she's"],
	['the waiter', 'he ', "he's"], 
	['the girl', 'she ', "she's"],
	['the baby', 'it ', "it's", 'he ', "he's", 'she ', "she's"], #10
	['the boy', 'he ', "he's",],
	['the woman', 'she', "she's"],
	['the man', 'he ', "he's",],
	['the man', 'he ', "he's",],
	['the man', 'he ', "he's",],
	['the frog', 'it ', "it's", 'he ', "he's", 'she ', "she's"],
	['the girl', 'she ', "she's"],
	['the man', 'he ', "he's",],
	['the woman', 'she ', "she's"],
	['the girl', 'she ', "she's"], #20
	['the boy', 'he ', "he's",],
	['the woman', 'she ', "she's"],
	['the doctor', 'he ', "he's"],
	['the boy', 'he ', "he's",],
	['the dog', 'it ', "it's", 'he ', "he's", 'she ', "she's"],
	['the man', 'he ', "he's",],
	['the girl', 'she ', "she's"],
	['the man', 'he ', "he's",],
	['the woman', 'she ', "she's"],
	['the woman', 'she ', "she's"]
	]

def sort_for_untargeted(n):
	yesRows=[]
	manualRows=[]
	inFileName='I'+str(n).zfill(2)+'T_Answer-'+hour+'.csv'
	subjVars = subjects[n-1]
	with open(inFileName) as inFile:
		inFReader=csv.reader(inFile, dialect=csv.excel)
		skipheader=next(inFReader, None)
		for irow in inFReader:
			if irow[-1].strip() == '1':
				subjFound=0
				for sv in subjVars:
					if sv in irow[0]:
						subjFound+=1
				if subjFound > 0:
					yesRows.append(irow[0])
				else:
					manualRows.append(irow[0])
			else:
				manualRows.append(irow[0])
	outFileNameManual='I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'  ##these will be annotated manually, so I give them the standard name so they'll be easier to run through the annotation interface
	outFileNameYes='I'+str(n).zfill(2)+'U_Answer-'+hour+'TEMP-YES.csv'  ##these will be automatically annotated as 'yes' and written to file; the file will eventually be remerged with the manually annotated output
	yesFile=open(outFileNameYes, 'w')
	yesWriter=csv.writer(yesFile, dialect=csv.excel)
	manualFile=open(outFileNameManual, 'w')
	manualWriter=csv.writer(manualFile, dialect=csv.excel)
	headRow=['I'+str(n).zfill(2)+'U', 'I'+str(n).zfill(2)+'U_Answer']
	yesWriter.writerow(headRow)
	manualWriter.writerow(headRow)
	for yr in yesRows:
		yesWriter.writerow([yr, '1'])
	yesFile.close()
	for mr in manualRows:
		manualWriter.writerow([mr])
	manualFile.close()

def main():
	for num in range(1,31):
		sort_for_untargeted(num)
		
if __name__ == "__main__":
    main()
