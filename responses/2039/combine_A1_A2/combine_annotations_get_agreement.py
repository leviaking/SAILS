#!/usr/bin/env python

##This script combines the annotations from annotator 1 and annotator 2, which it writes to a file and adds a column to indicate agreement. The two annotator files should be named like this:
##A1secondpassanno_I21T_Core-2039.csv
##A2secondpassanno_I41T_Core-2039.csv
##These files must be stored in the same folder. The command is like this, and takes only one argument, which is the filename for the A1 file.
##python combine_annotations_get_agreement.py A1secondpassanno_I01T_Answer-2039.csv
##The combined file will be output to the same location and named as this:
##agreesecondpassanno_I41T_Core-2039.csv

import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

##csvU is unsorted, csvS is sorted

anno1=sys.argv[1]
anno2=anno1.replace('A1', 'A2')
combined=anno1.replace('A1', 'agree')

anno1file=open(anno1, 'r')
anno1reader=csv.reader(anno1file, dialect=csv.excel)
anno1rows=[]
skipheader=next(anno1reader, None)
for a1row in anno1reader:
	anno1rows.append(a1row)
anno1file.close()

anno2file=open(anno2, 'r')
anno2reader=csv.reader(anno2file, dialect=csv.excel)
anno2rows=[]
skipheader=next(anno2reader, None)
for a2row in anno2reader:
	anno2rows.append(a2row)
anno2file.close()

masterheader=[skipheader[0], 'A1', 'A2', 'Agree']
combinedrows=[masterheader]
for a1row in anno1rows:
	a1resp = a1row[0]
	for a2row in anno2rows:
		if a1resp.strip()==a2row[0].strip():
			a1anno=a1row[1]
			a2anno=a2row[1]
			if a1anno==a2anno:
				agree='1'
			else:
				agree='0'
			crow = [a1resp, a1anno, a2anno, agree]
			combinedrows.append(crow)
		else:
			pass

combinedfile=open(combined, 'w')
combinedwriter=csv.writer(combinedfile, dialect=csv.excel)
for c in combinedrows:
	combinedwriter.writerow(c)
combinedfile.close()
