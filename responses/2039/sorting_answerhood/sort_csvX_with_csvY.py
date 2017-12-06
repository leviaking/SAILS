#!/usr/bin/env python

##This script operates on all 60 PDT items. Some annotation files are not sorted in the desired order, so this sorts one file according to another. For each item, it takes in csvU (unsorted) and csvS (sorted) and rewrites csvU in the order of csvS. The user should specify the filename (and path if necessary) for the csvU and csvS for item 01; the script will attempt to operate on all 60 items following the path and filename conventions from item 01.

import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

##csvU is unsorted, csvS is sorted
csvUseed = sys.argv[1]
csvUseed = sys.argv[1]
csvUparts= csvUseed.split('01')
csvUnose=csvUparts[0]
csvUtail=csvUparts[1]
csvSseed = sys.argv[2]
csvSparts = csvSseed.split('01')
csvSnose = csvSparts[0]
csvStail=csvSparts[1]
if not os.path.exists('csvUnsorted_Temp_BKP/'):
    os.makedirs('csvUnsorted_Temp_BKP/')

for n in range(1,31):
	csvUfilename = csvUnose+str(n).zfill(2)+csvUtail
	csvSfilename = csvSnose+str(n).zfill(2)+csvStail
	csvU = open(csvUfilename, 'r')
	#with open(csvUfilename) as csvU:
	csvUreader=csv.reader(csvU, dialect=csv.excel)
	csvUheadrow=next(csvUreader, None)
	csvUrows = []
	for csvUrow in csvUreader:
		csvUrows.append(csvUrow)
	csvU.close()
	copyfile(csvUfilename, 'csvUnsorted_Temp_BKP/'+csvUfilename)
	os.remove(csvUfilename)
	csvUoutput = [csvUheadrow] #this will be the properly sorted list of rows
	with open(csvSfilename) as csvS:
		csvSreader = csv.reader(csvS, dialect=csv.excel)
		csvSheadrow=next(csvSreader, None) ##we don't really need this but want to skip it
		for csvSrow in csvSreader:
			csvSresponse = csvSrow[0].strip()
			for cU in csvUrows:
				if cU[0].strip()==csvSresponse:
					csvUoutput.append(cU)
					break
	csvU = open(csvUfilename, 'w')
	csvUwriter = csv.writer(csvU, dialect=csv.excel)
	for Uo in csvUoutput:
		csvUwriter.writerow(Uo)
	csvU.close()

# fruits=['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
# lostfruits=['banana', 'fig', 'cherry']
# def find_fruit_continue(x):
# 	fruitindex=0
# 	for f in fruits:
# 		fruitindex+=1
# 		print fruitindex
# 		if f == x:
# 			print 'Found fruit at '+str(fruitindex)
# 			continue
# 
# def find_fruit_break(x):
# 	fruitindex=0
# 	for f in fruits:
# 		fruitindex+=1
# 		print fruitindex
# 		if f == x:
# 			print 'Found fruit at '+str(fruitindex)
# 			break
# for lf in lostfruits:
# 	find_fruit_continue(lf)
# 
# print '####################'
# 
# for lf in lostfruits:
# 	find_fruit_break(lf)
	
	# 
	# 
	# backupresponses=[]
	# annotatedresponses=[]
	# outheader=['I'+str(n).zfill(2)+'T', 'I'+str(n).zfill(2)+'T_Answer']
	# with open(backupfilename) as backupfile:
	# 	backupreader=csv.reader(backupfile, dialect=csv.excel)
	# 	skipheader=next(backupreader, None)
	# 	for brow in backupreader:
	# 		backupresponses.append(brow[0])
	# with open(automaticfilename) as automaticfile:
	# 	automaticreader=csv.reader(automaticfile, None)
	# 	skipheader=next(automaticreader, None)
	# 	for arow in automaticreader:
	# 		annotatedresponses.append(arow)
	# with open(manualfilename) as manualfile:
	# 	manualreader=csv.reader(manualfile, None)
	# 	skipheader=next(manualreader, None)
	# 	for mrow in manualreader:
	# 		annotatedresponses.append(mrow)
	# with open(outputfilename, 'w') as outputfile:
	# #with open(outputfilename) as outputfile:
	# 	outputwriter=csv.writer(outputfile, dialect=csv.excel)
	# 	outputwriter.writerow(outheader)
	# 	for br in backupresponses:
	# 		for ar in annotatedresponses:
	# 			if ar[0]==br:
	# 				outputwriter.writerow(ar)
	# 				

	


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
