#!/usr/bin/env python

##LK 

import sys, re, csv, datetime, os
from shutil import copyfile

header=['ID', 'parse']
outfile=open('../stats/multiline_sandbox.csv', 'w')
outwriter=csv.writer(outfile, dialect=csv.excel)
outwriter.writerow(header)

ID1='response001'
ID2='response002'

parse1='''1 first line
1 second line
1 third line
1 fourth line'''
parse2='''2 first line
2 second line
2 third line
2 fourth line'''
parse2b=parse2.split('\n')
parse2='\n'.join(parse2b)
row1=[ID1, parse1]
row2=[ID2, parse2]

outwriter.writerow(row1)
outwriter.writerow(row2)

outfile.close()

####

infile=open('../stats/multiline_sandbox.csv', 'r')
inreader=csv.reader(infile, dialect=csv.excel)
##print from the files we just wrote -- this ensures that multilines are in fact saved/printed as multilines
for row in inreader:
	for thing in row:
		print thing
		print '\n\n'
	
infile.close()


