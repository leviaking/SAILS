#!/usr/bin/env python

## 2019/06/02. LK.
##[NOT SURE: this script will be run via the text_to_lemmatized_conll.sh shell script.] This operates on the full "master_anno" csv files. this script will simply extract the NNS responses from the master anno CSVs (which also contain ResponseID and 5 annotation fields) and save them in a text file, with one response per line -- this is the format currently required by the text_to_lemmatized_conll.sh script, and it's the easiest way to pipe this stuff through the Stanford parser. 

import sys, re, csv, datetime, os
from shutil import copyfile

master_csvpathname=sys.argv[1]  # passed from shell, this is a string of path-relative-to-script+filename for a master_anno csv file; will be: ../corpus/I01T_master_annoTOY.csv, etc.
master_csvpathnamelist=master_csvpathname.split('/')
basepathlist=list(master_csvpathnamelist[:-1])  # seems to be omitting subfolders to construct a path...?
basepath = '../responses'
txtpath = basepath+'/txt'
rawcsvpath = basepath+'/rawcsvs'
csvname=master_csvpathnamelist[-1]  # remove path, keep filename
csvprefixn = csvname.split('.')[0]  # remove extension, keep name
csvprefixq = csvprefixn.split('_')[0]  # 'I02U_master_anno" --> 'I02U'
csvprefix = csvprefixq+"_NNS"  # --> 'I02U_NNS'
textname=csvprefix+'.txt'  # text filename by adding ".txt"

## read in all lines from master_anno csv and keep in responselist
allresponselist=[]
csvfile=open(master_csvpathname, 'rU')
csvreader=csv.reader(csvfile, dialect=csv.excel)
skipheader=next(csvreader, None)
for row in csvreader:
	unsorted_response=row
	allresponselist.append(unsorted_response)
csvfile.close()

## from all response list, find only those from NNS speakers; with these, write
## Response, ResponseID, C, A, G, I, V (annotations) to intermediate "rawcsv"
nns_responses = []
for r in allresponselist:
	if r[13].strip() == '0':  ## check that row contains a response (not all participants completed each item)
		pass
	else:
		if 'gNNS' in r[12]:
			nns_responses.append([r[12], r[13], r[14], r[15], r[16], r[17], r[18]])
		else:
			pass
rawcsvname=rawcsvpath+'/'+csvprefix+'.csv'
rawcsvfile=open(rawcsvname, 'w')
csvwriter = csv.writer(rawcsvfile, dialect=csv.excel)
csvheader = ['ResponseID', 'Response', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif']
csvwriter.writerow(csvheader)
for nnsr in nns_responses:
	csvwriter.writerow(nnsr)
rawcsvfile.close()

## From responses (which is NNS only), pull out response; if no punctuation, add
## period; write response (sentence) to txt file
textfile=open(txtpath+'/'+textname, 'w')
for resp_row in nns_responses:
	resp = resp_row[1]
	resp=resp.strip()
	if resp[-1] not in ['.', '!', '?']:
		resp=resp+'.'
	else: pass
	textfile.write(resp+'\n')
textfile.close()
