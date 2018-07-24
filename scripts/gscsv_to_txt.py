#!/usr/bin/env python

## 2018/07/05. LK.
##this script will be run via the text_to_lemmatized_conll.sh shell script. at this point, I'm developing it to work on the GS csv files; it may need some modification when it's time to process the test responses. this script will simply extract the responses from the CSVs (which also contain ResponseID and 5 annotation fields) and save them in a text file, with one response per line -- this is the format currently required by the text_to_lemmatized_conll.sh script, and it's the easiest way to pipe this stuff through the Stanford parser. 

import sys, re, csv, datetime, os
from shutil import copyfile

csvpathname=sys.argv[1]
csvpathnamelist=csvpathname.split('/')
txtpath=list(csvpathnamelist[:-2])
txtpath='/'.join(txtpath+['/txt'])
csvname=csvpathnamelist[-1]
textprefix = csvname.split('.')[0]
textname=textprefix+'.txt'

responselist=[]
csvfile=open(csvpathname, 'rU')
csvreader=csv.reader(csvfile, dialect=csv.excel)
skipheader=next(csvreader, None)
for row in csvreader:
	response=row[1]
	responselist.append(response)
csvfile.close()

textfile=open(txtpath+'/'+textname, 'w')
for resp in responselist:
	resp=resp.strip()
	if resp[-1] not in ['.', '!', '?']:
		resp=resp+'.'
	else: pass
	textfile.write(resp+'\n')
textfile.close()
