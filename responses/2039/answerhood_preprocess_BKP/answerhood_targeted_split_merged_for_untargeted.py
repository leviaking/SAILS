#!/usr/bin/env python

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
	inFileName='I'+str(n).zfill(2)+'T_Answer-'+hour+'.csv'
	outFileNameManual='I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'  ##these will be annotated manually, so I give them the standard name so they'll be easier to run through the annotation interface
	outFileNameYes='I'+str(n).zfill(2)+'U_Answer-'+hour+'TEMP-YES.csv'  ##these will be automatically annotated as 'yes' and written to file; the file will eventually be remerged with the manually annotated output
	

	

def merge(itemnum):
	rejectFile='rejected/REJECTED_I'+str(itemnum).zfill(2)+'T_Answer-'+hour+'.csv'
	manualFile='Answer/anno_I'+str(itemnum).zfill(2)+'T_Answer-'+hour+'.csv'
	mergedFile='TempMerged/TempMerged_I'+str(itemnum).zfill(2)+'T_Answer-'+hour+'.csv'
	copyfile(manualFile, mergedFile)
	mf = open(mergedFile, 'a')
	mfwriter=csv.writer(mf, dialect=csv.excel)
	with open(rejectFile, 'r') as rf:
		rfreader = csv.reader(rf, dialect=csv.excel)
		skipheader=next(rfreader, None)
		for rfrow in rfreader:
			rfrow=[rfrow[0], '0']
			mfwriter.writerow(rfrow)
	mf.close()
	checklines(itemnum, rejectFile, manualFile, mergedFile)
	
def checklines(i, r, m, g):
	print i
	rfo = open(r, 'r')
	rc = sum(1 for row in rfo)
	rfo.close()
	mfo = open(m, 'r')
	mc = sum(1 for row in mfo)
	mfo.close()
	gfo = open(g, 'r')
	gc = sum(1 for row in gfo)
	gfo.close()
	print rc, ' + ', mc, ' = ', (rc+mc), ' | merged: ', gc
	
	


def main():
	for num in range(1,31):
		sort_for_untargeted(num)
		
if __name__ == "__main__":
    main()
