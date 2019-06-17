#!/usr/bin/env python

##[For all items] This script takes in three files: an unnanotated master csv of untargeted response types in the original order (same order as in other features), a csv of responses that were "automatically" annotated based on the targeted annotations, and a csv of responses that were manually annotated. The unnanotated master file was split into the manual annotation file and the automatic annotation file -- this script will merge the files and output a single annotated file as "anno_"+filename.


import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

for n in range(1,31):
	backupfilename='BACKUP/BACKUP_I'+str(n).zfill(2)+'T_Answer-'+hour+'.csv'
	automaticfilename='AUTO/I'+str(n).zfill(2)+'T_Answer-'+hour+'ANNOTATED-YES.csv'
	manualfilename='MANUAL/MANUAL_I'+str(n).zfill(2)+'T_Answer-'+hour+'.csv'
	outputfilename='OUTPUT/I'+str(n).zfill(2)+'T_Answer-'+hour+'.csv'
	backupresponses=[]
	annotatedresponses=[]
	outheader=['I'+str(n).zfill(2)+'T', 'I'+str(n).zfill(2)+'T_Answer']
	with open(backupfilename) as backupfile:
		backupreader=csv.reader(backupfile, dialect=csv.excel)
		skipheader=next(backupreader, None)
		for brow in backupreader:
			backupresponses.append(brow[0])
	with open(automaticfilename) as automaticfile:
		automaticreader=csv.reader(automaticfile, None)
		skipheader=next(automaticreader, None)
		for arow in automaticreader:
			annotatedresponses.append(arow)
	with open(manualfilename) as manualfile:
		manualreader=csv.reader(manualfile, None)
		skipheader=next(manualreader, None)
		for mrow in manualreader:
			annotatedresponses.append(mrow)
	with open(outputfilename, 'w') as outputfile:
	#with open(outputfilename) as outputfile:
		outputwriter=csv.writer(outputfile, dialect=csv.excel)
		outputwriter.writerow(outheader)
		for br in backupresponses:
			for ar in annotatedresponses:
				if ar[0]==br:
					outputwriter.writerow(ar)
					

	


##read in BACKUP (master list)
##read in ANNOTATEDYES (automatic)
##read in MANUAL
##combine auto & manual as ANNOTATED
##outputrows = []
##for bac in BACKUP:
##	for ann in ANNOTATED:
##		if ann[0] == bac:
##			outputrows.append(ann)
##			break
##
##for opr in outputrows:
##write to csvout

# master=['apple', 'cookie', 'hamster']
# auto=[['pizza', 1], ['apple', 1], ['rat', 1]]
# manual=[['cookie', 2], ['apple', 2], ['turkey', 2], ['hamster', 2], ['blanket', 2]]
# 
# for m in master:
# 	for a in auto:
		


# 
# def applyAnnotation(n):
# 	RawResponses = []
# 	YesU=[] ##Yes Untargeted 
# 	AnnoFileName='I'+str(n).zfill(2)+'U_Answer-'+hour+'TEMP-YES.csv'
# 	RawFileName='I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'
# 	with open(RawFileName) as RawFile:
# 		RawReader=csv.reader(RawFile, dialect=csv.excel)
# 		skiprawheader=next(RawReader, None)
# 		for rrow in RawReader:
# 			RawResponses.append(rrow[0])
# 	with open(AnnoFileName) as AnnoFile:
# 		AnnoReader=csv.reader(AnnoFile, dialect=csv.excel)
# 		skipheader=next(AnnoReader, None)
# 		for arow in AnnoReader:
# 			if arow[0] in RawResponses:
# 				YesU.append(arow[0])
# 				RawResponses.remove(arow[0])
# 			else: pass
# 	copyfile(RawFileName, 'answerhood_backup/BACKUP_'+RawFileName)
# 	os.remove(RawFileName)
# 
# 	RawOutFileName = 'I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'  ##these will be annotated manually, so I give them the standard name so they'll be easier to run through the annotation interface
# 	AnnoOutFileName = 'I'+str(n).zfill(2)+'U_Answer-'+hour+'ANNOTATED-YES.csv'  ##these will be automatically annotated as 'yes' and written to file; the file will eventually be remerged with the manually annotated output
# 	ROF=open(RawOutFileName, 'w')
# 	AOF=open(AnnoOutFileName, 'w')
# 	RWriter=csv.writer(ROF, dialect=csv.excel)
# 	AWriter=csv.writer(AOF, dialect=csv.excel)
# 	headRow=['I'+str(n).zfill(2)+'U', 'I'+str(n).zfill(2)+'U_Answer']
# 	RWriter.writerow(headRow)
# 	AWriter.writerow(headRow)
# 	for y in YesU:
# 		AWriter.writerow([y, '1'])
# 	AOF.close()
# 	for r in RawResponses:
# 		RWriter.writerow([r])
# 	ROF.close()
# 
# def main():
# 	for num in range(1,31):
# 		applyAnnotation(num)
# 		
# if __name__ == "__main__":
#     main()
