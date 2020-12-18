#!/usr/bin/env python


## This is for calculating main verb type-to-token ratios for the development set and test set used for the holistic preference task, which was used to establish feature weights. The output of this script went directly into a table in Chapter 4 (Currently Table 4.3).

import sys, csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch
import random


nns_dev_t = "/Users/leviking/Documents/dissertation/SAILS/test_data/pool/I03T_NNS_test_pool.csv"
ns_dev_t = "/Users/leviking/Documents/dissertation/SAILS/training_data/pool/I03T_training_pool.csv"
nns_dev_u = "/Users/leviking/Documents/dissertation/SAILS/test_data/pool/I03U_NNS_test_pool.csv"
ns_dev_u = "/Users/leviking/Documents/dissertation/SAILS/training_data/pool/I03U_training_pool.csv"

nns_test_t = "/Users/leviking/Documents/dissertation/SAILS/test_data/pool/I28T_NNS_test_pool.csv"
ns_test_t = "/Users/leviking/Documents/dissertation/SAILS/training_data/pool/I28T_training_pool.csv"
nns_test_u = "/Users/leviking/Documents/dissertation/SAILS/test_data/pool/I28U_NNS_test_pool.csv"
ns_test_u = "/Users/leviking/Documents/dissertation/SAILS/training_data/pool/I28U_training_pool.csv"


def ch_4_numbers():
	print("NNS dev set T:")
	mytt = get_tt(nns_dev_t)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NS dev set T:")
	mytt = get_tt(ns_dev_t)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NNS dev set U:")
	mytt = get_tt(nns_dev_u)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NS dev set U:")
	mytt = get_tt(ns_dev_u)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NNS test set T:")
	mytt = get_tt(nns_test_t)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NS test set T:")
	mytt = get_tt(ns_test_t)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NNS test set U:")
	mytt = get_tt(nns_test_u)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")

	print("NS test set U:")
	mytt = get_tt(ns_test_u)
	print(mytt)
	print(float(mytt[0]/mytt[1]))
	print("\n###############################\n")


def get_tt(my_csv):
	my_verbs = get_verb_tokens(my_csv)
	tt_tuple = tokens_to_types(my_verbs)
	return tt_tuple


def get_verb_tokens(source_csv):
	raw_df = pd.read_csv(source_csv, index_col=0)
	xdh = raw_df["xdh"]
	verbs = []
	for xl in xdh:  ##xl is an ugly list-as-string: "['x$@%the$@%man', 'x$@%man$@%deliver', ...]"
		xl = xl[1:-1]
		xl = xl.replace("'", "")
		xl = xl.split(", ")
		for x in xl:
			if "$@%VROOT" in x:
				verbs.append(x)
	return verbs
	
		
def tokens_to_types(my_tokens):
	my_types = list(set(my_tokens))
	print(str(len(my_types))+" : "+str(len(my_tokens)))
	return (len(my_types), len(my_tokens))


def main():
	ch_4_numbers()


if __name__ == "__main__":
    main()
