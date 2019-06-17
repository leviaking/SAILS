#!/usr/bin/env python

##This script operates on all 60 PDT items. Because grammaticality is assessed without any PDT item context, the targeted and untargeted responses were combined into one set of response types, and these were annotated and output as a single file. I now need to use this file to apply the annotations to a file of targeted response types and a separate file of untargeted response types. Note that some response types appear in both the targeted and untargeted sets.

import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'



# # # ##csvU is unsorted, csvS is sorted
# csvUseed = sys.argv[1]
csvAseed = sys.argv[1] 
csvAparts= csvAseed.split('01')
csvAnose=csvAparts[0]
csvAtail=csvAparts[1]
# csvSseed = sys.argv[2]
# csvSparts = csvSseed.split('01')
# csvSnose = csvSparts[0]
# csvStail=csvSparts[1]
# if not os.path.exists('csvUnsorted_Temp_BKP/'):
#     os.makedirs('csvUnsorted_Temp_BKP/')

#for n in range(1,31):
for n in range(1,4):
	csvAfilename = csvAnose+str(n).zfill(2)+csvAtail
	csvA = open(csvAfilename, 'r')
	csvAreader=csv.reader(csvA, dialect=csv.excel)
	csvAheadrow=next(csvAreader, None)
	csvArows = []
	for csvArow in csvAreader:
		csvArows.append(csvArow)
	csvA.close()
	csvTrawfilename = 'Raw/I'+str(n).zfill(2)+'T_Raw-2039.csv'
	csvToutfilename = 'Gramm/anno_I'+str(n).zfill(2)+'T_Gramm-2039.csv'
	csvTheadrow = ['I'+str(n).zfill(2)+'T', 'I'+str(n).zfill(2)+'T_Gramm']
	csvToutput = [csvTheadrow]
	with open(csvTrawfilename) as csvTraw:
		csvTrawreader = csv.reader(csvTraw, dialect=csv.excel)
		junkheadrow=next(csvTrawreader, None) ##we don't really need this but want to skip it
		for csvTrawrow in csvTrawreader:
			csvTrawresponse = csvTrawrow[0].strip()
			for cA in csvArows:
				if cA[0].strip()==csvTrawresponse:
					csvToutput.append(cA)
					break
	csvUrawfilename = 'Raw/I'+str(n).zfill(2)+'U_Raw-2039.csv'
	csvUoutfilename = 'Gramm/anno_I'+str(n).zfill(2)+'U_Gramm-2039.csv'
	csvUheadrow = ['I'+str(n).zfill(2)+'U', 'I'+str(n).zfill(2)+'U_Gramm']
	csvUoutput = [csvUheadrow]
	with open(csvUrawfilename) as csvUraw:
		csvUrawreader = csv.reader(csvUraw, dialect=csv.excel)
		junkheadrow=next(csvUrawreader, None) ##we don't really need this but want to skip it
		for csvUrawrow in csvUrawreader:
			csvUrawresponse = csvUrawrow[0].strip()
			for cA in csvArows:
				if cA[0].strip()==csvUrawresponse:
					csvUoutput.append(cA)
					break
				
				
	csvToutfile = open(csvToutfilename, 'w')
	csvTwriter = csv.writer(csvToutfile, dialect=csv.excel)
	for csvTrow in csvToutput:
		csvTwriter.writerow(csvTrow)
	csvToutfile.close()
	csvUoutfile = open(csvUoutfilename, 'w')
	csvUwriter = csv.writer(csvUoutfile, dialect=csv.excel)
	for csvUrow in csvUoutput:
		csvUwriter.writerow(csvUrow)
	csvUoutfile.close()

