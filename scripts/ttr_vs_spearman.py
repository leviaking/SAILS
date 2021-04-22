#!/usr/bin/env python


## 2021/02/23. Adapted from get_stats_from_spearman.py
## Takes the csv of 360 Spearman scores and generates the desired averages (and
## other stats) according to parameters.


import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
import pandas
pandas.options.display.float_format = '{:.10f}'.format


def get_source_rows(tdf):
	## header row:
	"""Source	ldh_spear	ldh_p	xdh_spear	xdh_p	xdx_spear	xdx_p"""
	everything=[]
	tdoc=open(tdf, 'r')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def string_list_to_real_list(pylist):
	pylist = pylist[1:-1]
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%")
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist


def write_output(rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


def get_spearman_dict(rws):
	sources = []
	sdict = {}
	# ldh_sd = {}
	# xdh_sd = {}
	# xdx_sd = {}
	for rw in rws:
		srcn = rw[0]
		# ldh_k = srcn.replace("-r1-", "-r1-ldh-")
		# ldh_k = ldh_k.replace("-r2-", "-r2-ldh-")
		sources.append(srcn)
		# xdh_k = srcn.replace("-r1-", "-r1-xdh-")
		# xdh_k = xdh_k.replace("-r2-", "-r2-xdh-")
		# sources.append(xdh_k)
		# xdx_k = srcn.replace("-r1-", "-r1-xdx-")
		# xdx_k = xdx_k.replace("-r2-", "-r2-xdx-")
		# sources.append(xdx_k)
		# sdict[srcn] = [float(rw[1]), float(rw[2])]
		sdict[srcn] = float(rw[1])
		# sdict[xdh_k] = [float(rw[3]), float(rw[4])]
		# sdict[xdx_k] = [float(rw[5]), float(rw[6])]
	return sources, sdict


def get_ldh_ttr(source_name):
	training_name = source_name.replace("-VS-"+test_sample, ".csv")
	tr_header, tr_rows = get_source_rows(training_dir+training_name)
	model_tokens = []
	for trw in tr_rows:
		row_tokens = string_list_to_real_list(trw[8])
		model_tokens += row_tokens
	model_types = list(set(model_tokens))
	model_ttr = float(len(model_types)/len(model_tokens))
	return model_ttr
		

		
# ['det$@%the$@%boy', 'xsubj$@%boy$@%dancing', 'root$@%appear$@%VROOT', 'aux$@%to$@%dancing', 'aux$@%be$@%dancing', 'xcomp$@%dancing$@%appear', 'punct$@%.$@%appear']


train_sample = "N50"
weighted = "no"
test_sample = "N70"
stats_dir = "/Users/leviking/Documents/dissertation/SAILS/stats/"
training_dir = ("/Users/leviking/Documents/dissertation/SAILS/"+
				"training_data/"+train_sample+"/")

def main():
	if weighted == "yes":
		working_dir=(stats_dir+train_sample+'-VS-'+test_sample+'-W/')
		all_spearman_file = "all_spearman_"+train_sample+"-VS-"+test_sample+"-W.csv"
	else:
		working_dir=(stats_dir+train_sample+'-VS-'+test_sample+'/')
		all_spearman_file = "all_spearman_"+train_sample+"-VS-"+test_sample+".csv"
	oldheader, all_spearman_rows = get_source_rows(working_dir+all_spearman_file)
	# oldheader = ["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]
	all_sources, s_dict = get_spearman_dict(all_spearman_rows)  ## ['I01T-gNSC-r1-In-N50-VS-N70', ...], {'I01T-gNSC-r1-In-N50-VS-N70': 0.2571727}
	# print(s_dict)
	outrows = [["Source", "ldh_ttr", "ldh_Spearman"]]
	for sr in all_sources:
		# if "r1" and "-Tr-" in sr:
		# 	if "T-" in sr:
		# 		sr_spearman = s_dict[sr]
		# 		sr_ttr = get_ldh_ttr(sr)
		# 		outrows.append([sr, sr_ttr, sr_spearman])
		sr_spearman = s_dict[sr]
		sr_ttr = get_ldh_ttr(sr)
		outrows.append([sr, sr_ttr, sr_spearman])
	outname = stats_dir+train_sample+"-VS-"+test_sample+"-models-ldh_ttr_vs_spearman.csv"
	write_output(outrows, outname)


if __name__ == "__main__":
    main()
