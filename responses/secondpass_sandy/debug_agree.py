#!/usr/bin/env python

import sys, csv, itertools, os

dfile=open('debug_file.csv', 'r')
dreader=csv.reader(dfile, dialect=csv.excel)
header=next(dreader, None)

outf=open('debug_output.csv', 'w')
outwriter=csv.writer(outf, dialect=csv.excel)
drows=[]
for drow in dreader:
	drows.append(drow)
	
dfile.close()

checkedpairs=[]

for h1 in header:
	headertwo=[x for x in header if x!=h1]
	for h2 in headertwo:
		if h1+h2 not in checkedpairs:
			checkedpairs.append(h1+h2)
			checkedpairs.append(h2+h1)
			#label=h1+'_'+h2
			h1h2agree=0.0
			total=0.0
			for drow in drows:
				#print drow
				h1an=drow[header.index(h1)]
				h2an=drow[header.index(h2)]
				if h1an==h2an:
					h1h2agree+=1.0
				else:
					pass
				total+=1
			agreement=float(h1h2agree/total)
			outwriter.writerow([h1, h2, str(agreement)])
		