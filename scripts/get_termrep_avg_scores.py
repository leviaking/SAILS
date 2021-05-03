#!/usr/bin/env python


## 2021/05/02. Adapted from annotation_features_average_precision.py
## For a given set of scores (e.g., N50 vs N70), this script iterates over all scored item files and calculates an average response score (i.e., distance from NS model) for ldh, xdh, xdx. I'm using this to support claim in Chapter 6: where NS and NNS behavior is less convergent (intransitives and ditransitives), xdx works best because it reduces the distance between NS and NNS, but for transitives, where behavior is more convergent, using more granular representation (ldh) performs well. So the numbers I get from this script need to confirm that w.r.t. to distance from the NS model: xdx < xdh < xdx .

import sys, math, csv, pandas, random
import numpy as np
from sklearn.metrics import average_precision_score
from os import walk
from scipy.stats import rankdata
pandas.options.display.float_format = '{:.3f}'.format



def get_input_file_names(input_dir): 
	input_file_names = []
	for (dirpath, dirnames, filenames) in walk(input_dir):
		input_file_names.extend(filenames)
		break
	input_file_names = [j for j in input_file_names if j.endswith(".csv")]
	input_file_names.sort()
	return input_file_names


def get_termrep_avg_scores(input_dir, input_fns):
	z_ldh = []
	z_xdh = []
	z_xdx = []
	# mycols = ['ResponseID', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif', 'AnnoRank', 'ldh TC', 'xdh TC', 'xdx TC', 'BERT_rank']
	for ipf in input_fns:
		ipdf = pandas.read_csv(input_dir+ipf, usecols=['ldh TC', 'xdh TC', 'xdx TC'])
		# ldh_tc = list(ipdf_raw['ldh TC'])
		# print(type(ldh_tc))
		z_ldh += list(ipdf['ldh TC'])
		z_xdh += list(ipdf['xdh TC'])
		z_xdx += list(ipdf['xdx TC'])
	av_ldh = sum(z_ldh)/len(z_ldh)
	av_xdh = sum(z_xdh)/len(z_xdh)
	av_xdx = sum(z_xdx)/len(z_xdx)
	print(av_ldh)
	print(av_xdh)
	print(av_xdx)
	print(len(z_ldh))
	print(len(z_xdh))
	print(len(z_xdx))

# def write_output(rs, nm):
# 	outdir =('/Users/leviking/Documents/dissertation/SAILS/average_precision/')
# 	thisfile=open(outdir+nm, 'w')
# 	thiswriter=csv.writer(thisfile, dialect=csv.excel)
# 	for r in rs:
# 		thiswriter.writerow(r)
# 	thisfile.close()


def main():
	my_input_dir = ("/Users/leviking/Documents/dissertation/SAILS/test_data/"+
					"scored/N50-VS-N70/")
					# "scored/N14-VS-N70/")
					# "scored/F14-VS-N70/")
	my_inputs = get_input_file_names(my_input_dir)
	get_termrep_avg_scores(my_input_dir, my_inputs)



if __name__ == "__main__":
    main()
