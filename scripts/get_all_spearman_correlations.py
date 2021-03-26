#!/usr/bin/env python


## 2020/07/28. Branched from dependency_format_experiment.py
## This script operates on the directory of test files in which each test
## response in each test file already has a tf-idf cosine (TC) score;
## This script reads in the (annotation based) GS ranking and the model based
## ranking for each file and generates a Spearman correlation for the file.
## (Actually, because each file combines LDH, XDH and XDX formats, there are
## three scores per file.)
## Each Spearman score is saved and written to a single csv.

import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if ".csv" in dn]
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


def get_all_rankings(rrows):
	"""ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx	AnnoScore	AnnoRank	ldh TC	xdh TC	xdx TC"""
	anno_ranks = []
	ldh_scores = []
	xdh_scores = []
	xdx_scores = []
	for rr in rrows:
		anno_ranks.append(rr[12])  ## M
		ldh_scores.append(rr[13])  ## N
		xdh_scores.append(rr[14])  ## O
		xdx_scores.append(rr[15])  ## P
	ldh_ranks = list(rankdata(ldh_scores).astype(float))  ## e.g. if m=[8, 0.5, 11, 9] then list(rankdata(m)) = [2, 1, 4, 3]
	xdh_ranks = list(rankdata(xdh_scores).astype(float))
	xdx_ranks = list(rankdata(xdx_scores).astype(float))
	spearman_row = calculate_spearman([anno_ranks, ldh_ranks, xdh_ranks, xdx_ranks])
	extended_rows = []
	for rr in rrows:
		xr = rr+[ldh_ranks.pop(0), xdh_ranks.pop(0), xdx_ranks.pop(0)]
		extended_rows.append(xr)
	return extended_rows, spearman_row


def calculate_spearman(allranks):
	## spearman values will go in a csv with this header:
	## (Source), ldh_w_spearman, ldh_w_p, xdh_w_spearman, xdh_w_p, xdx_w_spearman, xdx_w_p, ldh_uw_spearman, ldh_uw_p, xdh_uw_spearman, xdh_uw_p, xdx_uw_spearman, xdx_uw_p
	anno_ranks = allranks[0]
	ldh_ranks = allranks[1]
	xdh_ranks = allranks[2]
	xdx_ranks = allranks[3]
	ldh_spr, ldh_p = spearmanr(ldh_ranks, anno_ranks)
	xdh_spr, xdh_p = spearmanr(xdh_ranks, anno_ranks)
	xdx_spr, xdx_p = spearmanr(xdx_ranks, anno_ranks)
	sp_row = [ldh_spr, ldh_p, xdh_spr, xdh_p, xdx_spr, xdx_p]
	return sp_row


def process_one_item(somefile):
	## do all the above, return item rows and spearman scores
	oldheader, sourcerows = get_source_rows(somefile)
	newheader = oldheader+['ldh rank', 'xdh rank', 'xdx rank']
	rows_with_ranks, spearman_row = get_all_rankings(sourcerows)
	rows_with_ranks.insert(0, newheader)
	return rows_with_ranks, spearman_row


def write_output(rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


def main():
	train_sample = "F14"
	test_sample = "N70"
	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'+
			   train_sample+'-VS-'+test_sample+'/')
	statsdir=('/Users/leviking/Documents/dissertation/SAILS/stats/'+
			   train_sample+'-VS-'+test_sample+'/')
	input_files = get_infile_names(sourcedir)
	spearman_rows = [["Source", "ldh_spear", "ldh_p", "xdh_spear", "xdh_p", "xdx_spear", "xdx_p"]]
	for inf in input_files:
		print(inf)
		out_label = inf.replace(".csv", "")
		output_rows, spearman_row = process_one_item(sourcedir+inf)
		spearman_row.insert(0, out_label)
		spearman_rows.append(spearman_row)
		# write_output(output_rows, sourcedir+inf)
	write_output(spearman_rows, statsdir+"/all_spearman_"+
				 train_sample+'-VS-'+test_sample+".csv")


if __name__ == "__main__":
    main()
