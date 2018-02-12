#!/usr/bin/env python

##[FOR EACH ITEM:] This script takes in a file containing answerhood annotations for targeted responses; this file has been filtered to contain only responses which should receive the same annotation under targeted and untargeted conditions. This script also takes in the unannotated file of untargeted responses. The script iterates through the targeted responses, looks for a match in the untargeted responses, and applies the targeted annotation to the untargeted response. Note that the targeted list contains only "yes" ("1") annotated responses.


import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

def applyAnnotation(n):
	RawResponses = []
	YesU=[] ##Yes Untargeted 
	AnnoFileName='I'+str(n).zfill(2)+'U_Answer-'+hour+'TEMP-YES.csv'
	RawFileName='I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'
	with open(RawFileName) as RawFile:
		RawReader=csv.reader(RawFile, dialect=csv.excel)
		skiprawheader=next(RawReader, None)
		for rrow in RawReader:
			RawResponses.append(rrow[0])
	with open(AnnoFileName) as AnnoFile:
		AnnoReader=csv.reader(AnnoFile, dialect=csv.excel)
		skipheader=next(AnnoReader, None)
		for arow in AnnoReader:
			if arow[0] in RawResponses:
				YesU.append(arow[0])
				RawResponses.remove(arow[0])
			else: pass
	copyfile(RawFileName, 'answerhood_backup/BACKUP_'+RawFileName)
	os.remove(RawFileName)

	RawOutFileName = 'I'+str(n).zfill(2)+'U_Answer-'+hour+'.csv'  ##these will be annotated manually, so I give them the standard name so they'll be easier to run through the annotation interface
	AnnoOutFileName = 'I'+str(n).zfill(2)+'U_Answer-'+hour+'ANNOTATED-YES.csv'  ##these will be automatically annotated as 'yes' and written to file; the file will eventually be remerged with the manually annotated output
	ROF=open(RawOutFileName, 'w')
	AOF=open(AnnoOutFileName, 'w')
	RWriter=csv.writer(ROF, dialect=csv.excel)
	AWriter=csv.writer(AOF, dialect=csv.excel)
	headRow=['I'+str(n).zfill(2)+'U', 'I'+str(n).zfill(2)+'U_Answer']
	RWriter.writerow(headRow)
	AWriter.writerow(headRow)
	for y in YesU:
		AWriter.writerow([y, '1'])
	AOF.close()
	for r in RawResponses:
		RWriter.writerow([r])
	ROF.close()

def main():
	for num in range(1,31):
		applyAnnotation(num)
		
if __name__ == "__main__":
    main()
