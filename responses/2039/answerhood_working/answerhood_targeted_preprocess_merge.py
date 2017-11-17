#!/usr/bin/env python

##This script will merge the auto-rejected (based on regex) responses with the manually annotated remainder. This is an intermediate step for Answerhood (untargeted) annotation.

import sys, csv
from shutil import copyfile

hour = '2039'

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
	for n in range(1,31):
		merge(n)
		
if __name__ == "__main__":
    main()
