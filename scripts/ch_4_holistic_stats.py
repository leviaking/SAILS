#!/usr/bin/env python


## 2020-12-12: This is for generating descriptive stats based on the weighted annotation scores; comparing various groups & subsets, e.g., NS vs NNS.

import pandas as pd
from os import walk


nns_dir = "/Users/leviking/Documents/dissertation/SAILS/test_data/pool/"
nns_tags = ["NNS_"]
ns_dir = "/Users/leviking/Documents/dissertation/SAILS/training_data/sets/"
ns_tags = ["gNS"]
# cns_tags = ["gNSC", "I02T", "r1", "Tr"]
cns_tags = ["gNSC"]
fns_tags = ["gNSF"]
cns_r1_tags = ["gNSC", "r1"]
cns_r2_tags = ["gNSC", "r2"]
cns_intrans_tags = ["gNSC", "In-"]
cns_trans_tags = ["gNSC", "Tr-"]
cns_ditrans_tags = ["gNSC", "Di-"]
cns_targ_tags = ["T-gNSC"]
cns_untarg_tags = ["U-gNSC"]
# yy = "/Users/leviking/Documents/dissertation/SAILS/training_data/pool/I03T_training_pool.csv"


def get_infile_names(somedir, sometags): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	for sometag in sometags:
		docnames = [dn for dn in docnames if sometag in dn]
	docnames = [somedir+dn for dn in docnames]
	docnames.sort()
	return docnames


def get_one_doc_scores(source_csv):
	raw_df = pd.read_csv(source_csv, index_col=0)
	anno_scores = raw_df["AnnoScore"]
	return anno_scores


def get_all_docs_scores(my_docs):
	all_docs_scores = pd.Series(dtype="float64")
	for my_csv in my_docs:
		my_csv_scores = get_one_doc_scores(my_csv)
		all_docs_scores = all_docs_scores.append(my_csv_scores, ignore_index = True)
	return all_docs_scores


def get_descriptive_stats(my_scores):
	described = my_scores.describe()
	print(described)
	my_count = described["count"]
	# print("mycount: "+str(my_count))
	z = my_scores.value_counts()
	ones = z[1.000]
	zeros = z[0.000]
	print("perfects: "+str(ones)+"/"+str(my_count)+" = "+str(ones/my_count))
	print("zeros: \t"+str(zeros)+"/"+str(my_count)+" = "+str(zeros/my_count))
	print("\n")


def process_set(set_dir, set_tags):
	label = "+".join(set_tags)
	print("\n\n\n################BREAK################\n"+label+" stats:")
	all_docs = get_infile_names(set_dir, set_tags)
	all_scores = get_all_docs_scores(all_docs)
	get_descriptive_stats(all_scores)	


def main():
	process_set(nns_dir, nns_tags)
	process_set(ns_dir, ns_tags)
	process_set(ns_dir, cns_tags)
	process_set(ns_dir, fns_tags)
	process_set(ns_dir, cns_r1_tags)
	process_set(ns_dir, cns_r2_tags)
	process_set(ns_dir, cns_intrans_tags)
	process_set(ns_dir, cns_trans_tags)
	process_set(ns_dir, cns_ditrans_tags)
	process_set(ns_dir, cns_targ_tags)
	process_set(ns_dir, cns_untarg_tags)


if __name__ == "__main__":
    main()
