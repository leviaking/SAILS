#!/usr/bin/env python

## July 2020; This script needs to construct test sets of a consistent size drawn from pools of inconsistent size

import sys, csv
from os import walk


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir+"pool/"):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if "test_pool" in dn]
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
	for row in tdocreader:
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


def main():
	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/')
	input_files = get_infile_names(sourcedir)
	for inp in input_files:
		header, new_source_rows = get_source_rows(sourcedir+"pool/"+inp)
		# print(inp+":   "+str(len(new_source_rows)))
		sample_size = 70
		sample_fn = inp.replace("pool", "N"+str(sample_size))
		sample_fn = sample_fn.replace("_", "-")
		nsr = new_source_rows[:sample_size]
		print(inp+":   "+str(len(nsr)))
		write_output(header, nsr, sourcedir+"/N"+str(sample_size)+"/"+sample_fn)


if __name__ == "__main__":
    main()
