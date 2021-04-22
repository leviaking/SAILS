#!/usr/bin/env python

## July 2020; This script constructs test sets of a fixed size from pools of
## uneven sizes. It also calculates and writes out the rank for each response
## included in a new set.


import sys, csv
from os import walk
from scipy.stats import rankdata


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir+"pool/"):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if "test_pool" in dn]
	docnames.sort()
	return docnames


def get_source_rows(tdf):
	everything=[]
	tdoc=open(tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def get_annotation_ranks(rs):
	anno_scores = []
	for r in rs:
		anno_scores.append(float(r[11]))
	anno_ranks = list(rankdata(anno_scores).astype(float))
	anno_ranks = [float(len(anno_scores)) - r for r in anno_ranks]  ## This inverts the ranking -- I prefer to get spearman scores between 0 and 1 (not between 0 and -1)
	extended_rows = []
	for r in rs:
		xr = r+[anno_ranks.pop(0)]
		extended_rows.append(xr)
	return extended_rows


def write_output(hd, rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	thiswriter.writerow(hd)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


# def main():
# 	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/')
# 	input_files = get_infile_names(sourcedir)
# 	for inp in input_files:
# 		header, new_source_rows = get_source_rows(sourcedir+"pool/"+inp)
# 		header.append("AnnoRank")
# 		sample_size = 70
# 		sample_fn = inp.replace("pool", "N"+str(sample_size))
# 		sample_fn = sample_fn.replace("_", "-")
# 		nsr = new_source_rows[:sample_size]
# 		output_rows = get_annotation_ranks(nsr)
# 		print(inp+":   "+str(len(nsr)))
# 		write_output(header, output_rows, sourcedir+"/N"+str(sample_size)+"/"+sample_fn)


if __name__ == "__main__":
    main()
