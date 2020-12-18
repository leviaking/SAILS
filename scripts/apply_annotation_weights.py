#!/usr/bin/env python


## 2020-12-12. BE CAREFUL running this script as I have modified it... In particular
## note the "get_source_rows" function -- I currently have it stripping off
## any columns beyond the 11th column...

## This script operates on the test pool files, which are 1 per test item (60 total).
## This applies the annotation feature weights to the existing annotation for
## each response, yielding a single score for each response.
## NB: The annotation *rank* cannot be applied here because the rank of each
## item will depend on the other items in the *sample* -- this is the pool from
## which the sample is later drawn.


import sys, csv
from os import walk


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	# docnames = [dn for dn in docnames if "test_pool" in dn]
	# docnames = [dn for dn in docnames if "training_pool" in dn]
	docnames = [dn for dn in docnames if "N50" in dn]
	docnames.sort()
	return docnames



def get_source_rows(tdf): ## tdf ~= test doc file; returns csv lines as lists
# input header:
# ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx	ldh TC weighted	xdh TC weighted	xdx TC weighted	ldh TC unweighted	xdh TC unweighted	xdx TC unweighted
# scores are row[11] thru row[16]
	everything=[]
	tdoc=open(tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	skipheader = skipheader[:11]
	for row in tdocreader:
		row = row[:11]
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def write_output(hd, rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	thiswriter.writerow(hd)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


def apply_annotation_weights(somerows):
	extended_rows = []
	##annotations are on row[2] thru row[6] (CAGIV)
	## .365 + .093 + .056 + .224 + .262 == 1 (Use these)
	for sr in somerows:
		a_score = float(sr[2]) * 0.365
		a_score = a_score + (float(sr[3]) * 0.093)
		a_score = a_score + (float(sr[4]) * 0.056)
		a_score = a_score + (float(sr[5]) * 0.224)
		a_score = a_score + (float(sr[6]) * 0.262)
		sr.append(str(a_score))
		extended_rows.append(sr)
	## So this is returning the original row + AnnoScore
	return extended_rows


def main():
	# sourcedir=('/Users/leviking/Documents/dissertation/SAILS/training_data/sets/')
	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/training_data/N50/')
	# sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/pool/')
	input_files = get_infile_names(sourcedir)
	for inp in input_files:
		print(inp)
		header, new_source_rows = get_source_rows(sourcedir+inp)
		header.append("AnnoScore")
		output_rows = apply_annotation_weights(new_source_rows)
		write_output(header, output_rows, sourcedir+inp)


if __name__ == "__main__":
    main()
