#!/usr/bin/env python


## 2020/07/28. Branched from dependency_format_experiment.py
## This script takes in a single CSV that contains Spearman correlation scores
## for every model run on the test data. It groups these scores according to
## the parameters specified in this script, and writes out a set of descriptive
## stats for each model in the group, then writes a file for the group.


import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
import pandas


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	# # docnames = [dn for dn in docnames if "NNS_vs_all_ns_TC_w" in dn]
	docnames = [dn for dn in docnames if "NNS_vs_all_ns_TC_w" in dn]
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


def write_output(rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


def get_spearman_dict(rws):
	sd = {}
	for rw in rws:
		sd[rw[0]] = [rw[1], rw[3], rw[5]]
	return sd	


def get_per_item_stats(sd):
	ldh_all_stats = []
	xdh_all_stats = []
	xdx_all_stats = []
	for i in range(1,31):
		for targval in ["T", "U"]:
			item = "I"+str(i).zfill(2)+targval
			for model_name in sd:
				if item in model_name:
					ldh.append(sd[model_name][0])
					xdh.append(sd[model_name][1])
					xdx.append(sd[model_name][2])
			# write_output(ldh, model_name+"-ldh")


def main():
	working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/N70/")
	all_spearman_file = "all_spearman_N70.csv"
	# spearman_rows = [["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]]
	experiments = ["PerItem", "FirstVsMix", "Transitivity", "Targeting"]
	oldheader, all_spearman_rows = get_source_rows(working_dir+all_spearman_file)
	spearman_dict = get_spearman_dict(all_spearman_rows)
	get_per_item_stats(spearman_dict)

					
					
	
	
	
	
	for inf in input_files:
		out_label = inf.replace("_TC_w.csv", "")
		output_rows, spearman_row = process_one_item(sourcedir+inf)
		spearman_row.insert(0, out_label)
		spearman_rows.append(spearman_row)
		write_output(output_rows, outputdir+out_label+".csv")
	write_output(spearman_rows, outputdir+"dependency_format_experiment-all_ns-spearman.csv")


if __name__ == "__main__":
    main()
