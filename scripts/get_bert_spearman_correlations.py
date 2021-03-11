#!/usr/bin/env python


## 2021/03/01. Branched from get_all_spearman_correlations.py
## This script operates on the directory of test files in which each test
## response in each test file already has a tf-idf cosine (TC) score;
## This script reads in the (annotation based) GS ranking and the model based
## ranking for each file and generates a Spearman correlation for the file.
## (Actually, because each file combines LDH, XDH and XDX formats, there are
## three scores per file.)
## Each Spearman score is saved and written to a single csv.

from os import walk
from scipy.stats import spearmanr
import pandas as pd


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if ".csv" in dn]
	docnames.sort()
	return docnames


def process_spearman(raw_bird):
	# bird = pd.read_csv(bert_dir+raw_bird, index_col=0)
	bird = pd.read_csv(bert_dir+raw_bird)
	gold_ranks = bird["AnnoRank"]
	bert_ranks = bird["BERT_rank"]
	bsp, bpv = spearmanr(bert_ranks, gold_ranks)
	return bsp, bpv


def combine_csvs(bfull):
	# oldie = pd.read_csv(statsdir+"all_spearman_N70.csv", index_col=0)
	b = pd.DataFrame([bfull["BERT_spear"], bfull["BERT_p"]])
	oldie = pd.read_csv(statsdir+"all_spearman_N70.csv")
	newdf = pd.concat([oldie, b], axis=1)
	print(newdf)
	newdf.to_csv(statsdir+"/combined_spearman_"+test_sample+".csv", index=False)


train_sample = "N50"
test_sample = "N70"
bert_dir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'+
		  train_sample+'-VS-'+test_sample+'-BERT/')
statsdir=('/Users/leviking/Documents/dissertation/SAILS/stats/'+
		  train_sample+'-VS-'+test_sample+'/')


def main():
	b_rank_docs = get_infile_names(bert_dir)
	bspears = []
	bpvals = []
	blabels = []
	for brd in b_rank_docs:
		## transform the source label back to match the non-bert version
		blab = brd.replace("-BERT.csv", "")
		blab = blab.replace("-vs_r", "-r")
		blabels.append(blab)
		bspear, bpval = process_spearman(brd)
		bspears.append(bspear)
		bpvals.append(bpval)
	bdict = {"Source": blabels, "BERT_spear": bspears, "BERT_p": bpvals}
	bdf = pd.DataFrame(data=bdict)	
	bdf.to_csv(statsdir+"bert_spearman_"+train_sample+"-VS-"+test_sample+
			   ".csv", index=False)
	
	# b = pd.DataFrame([bfull["BERT_spear"], bfull["BERT_p"]])
	oldie = pd.read_csv(statsdir+"all_spearman_"+
						train_sample+"-VS-"+test_sample+".csv")
	newdf = pd.merge(oldie, bdf, on="Source")
	# print(newdf)
	newdf.to_csv(statsdir+"/combined_spearman_"+train_sample+"-VS-"+
				 test_sample+".csv", index=False)


if __name__ == "__main__":
    main()
