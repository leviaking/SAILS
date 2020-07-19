#!/usr/bin/env python

## LK 2020/07/18: BRANCHED FROM gs_assembler.py;
# This script takes in all GS files like this one:
## /Users/leviking/Documents/dissertation/SAILS/gold_standards/depstrings/I01T_all_ns_depstrings.csv
# And splits each up into k files containing j responses each;
# I'm planning to do k=5 for j=15 and j=50;
# The output should go here:
## /Users/leviking/Documents/dissertation/SAILS/gold_standards/cross-validation/depstrings/<j>/


import sys, re, csv, datetime, os, random
from shutil import copyfile


gstag='all_ns_depstrings'  ## or all_fns_depstrings, etc.
sourcedir='/Users/leviking/Documents/dissertation/SAILS/gold_standards/derps/'
targetdir='/Users/leviking/Documents/dissertation/SAILS/gold_standards/cross_validation/'
k=5  ## The number of sample files (e.g., 10 for 10-fold cross-val)
j=15  ## Number of responses in each sample


def get_sourcefile_list(sd):
	sourcefiles=[]
	for root, dirs, files in os.walk(sd):
		for name in files:
			if gstag in name:
				sourcefiles.append(name)
			else:
				pass
	sourcefiles.sort()
	return sourcefiles


def generate_sample_files(mysource):
	myfile=open(sourcedir+mysource, 'rU')
	myreader=csv.reader(myfile, dialect=csv.excel)
	header=next(myreader, None)
	pool = []
	for srow in myreader:
		pool.append(srow)
	for fold in range(1,k+1):
		foldtag = "_f"+str(fold)
		foldfilename = targetdir+str(j)+"/"+mysource.replace(".csv", foldtag+".csv")
		foldrows = []
		while len(foldrows) < j:
			myindex = random.randint(1,len(pool)-1)
			foldrows.append(pool[myindex])
		foldfile=open(foldfilename, 'w')
		foldwriter=csv.writer(foldfile, dialect=csv.excel)
		foldwriter.writerow(header)
		for frow in foldrows:
			foldwriter.writerow(frow)
		foldfile.close()


def main():
	sfiles=get_sourcefile_list(sourcedir)
	for sf in sfiles:
		generate_sample_files(sf)


if __name__ == "__main__":
    main()


# # XF recommends using these numbers for comparing Spearman:
# # lower 5, median, 95, average, standard deviation, maybe also min and max
## There should be a python command "describe"? that spits out many of the above measures;
## This analysis would be considered "descriptive statistics"
