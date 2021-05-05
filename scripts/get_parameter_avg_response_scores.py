#!/usr/bin/env python


## 2021/05/02. Adapted from annotation_features_average_precision.py
## For a given set of scores (e.g., N50 vs N70), this script iterates over all scored item files and calculates an average response score (i.e., distance from NS model) for ldh, xdh, xdx, targ, untarg, intrans, trans, ditrans, primary, mixed...  I'm using this to support various claims in Chapter 6, e.g., where NS and NNS behavior is less convergent (intransitives and ditransitives), xdx works best because it reduces the distance between NS and NNS, but for transitives, where behavior is more convergent, using more granular representation (ldh) performs well. So the numbers I get from this script need to confirm that w.r.t. to distance from the NS model: xdx < xdh < xdx .

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


def get_param_avg_scores(input_dir, input_fns):
	z_ldh = []
	z_xdh = []
	z_xdx = []
	z_bert = []
# paramd = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}
	z_intrans = []
	z_trans = []
	z_ditrans = []
	z_targ = []
	z_untarg = []
	z_crowd = []
	z_fam = []
	z_prim = []
	z_mix = []
	setting_list_d = {'T-': z_targ, 'U-': z_untarg, '-In-': z_intrans,
					  '-Tr-': z_trans, '-Di-': z_ditrans, '-gNSC-': z_crowd,
					  '-gNSF-': z_fam, 'r1-': z_prim, 'r2-': z_mix}
	# mycols = ['ResponseID', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif', 'AnnoRank', 'ldh TC', 'xdh TC', 'xdx TC', 'BERT_rank']
	for ipf in input_fns:
		print(ipf)
		ipdf = pandas.read_csv(input_dir+ipf, usecols=['ldh TC', 'xdh TC', 'xdx TC', 'BERT_score'])
		# ldh_tc = list(ipdf_raw['ldh TC'])
		# print(type(ldh_tc))
		curr_ldh = list(ipdf['ldh TC'])
		z_ldh += curr_ldh
		curr_xdh = list(ipdf['xdh TC'])
		z_xdh += curr_xdh
		curr_xdx = list(ipdf['xdx TC'])
		z_xdx += curr_xdx
		z_bert += list(ipdf['BERT_score'])
		curr_scores = curr_ldh+curr_xdh+curr_xdx
		curr_avg = sum(curr_scores)/len(curr_scores) ## for other params, we can just pass the average of the three termreps
		# print(curr_avg)
		for mx in my_exps:
			settings = paramd[mx]
			# print('\t'+mx)
			for sg in settings:
				# print('\t\t'+sg)
				if sg in ipf:
					# print('\t\t\tMATCH')
					setting_list_d[sg].append(curr_avg)
					# print(setting_list_d[sg])
	av_ldh = sum(z_ldh)/len(z_ldh)
	av_xdh = sum(z_xdh)/len(z_xdh)
	av_xdx = sum(z_xdx)/len(z_xdx)
	av_intrans = sum(z_intrans)/len(z_intrans)
	av_trans = sum(z_trans)/len(z_trans)
	av_ditrans = sum(z_ditrans)/len(z_ditrans)
	av_targ = sum(z_targ)/len(z_targ)
	av_untarg = sum(z_untarg)/len(z_untarg)
	av_intrans = sum(z_intrans)/len(z_intrans)
	try:
		av_prim = sum(z_prim)/len(z_prim)
	except:
		av_prim = "NA"
	av_mix = sum(z_mix)/len(z_mix)
	av_bert = sum(z_bert)/len(z_bert)
	
		# index_col = ['Intrans', 'Trans', 'Ditrans', 'Targ', 'Untarg', 'Prim',
		# 		 'Mixed', 'ldh', 'xdh', 'xdx', 'BERT']
	samp_avgs = [av_intrans, av_trans, av_ditrans, av_targ, av_untarg, av_prim,
				 av_mix, av_ldh, av_xdh, av_xdx, av_bert]
	print('ldh\tcount\tavg: ', len(z_ldh), '\t', av_ldh)
	print('xdh\tcount\tavg: ', len(z_xdh), '\t', av_xdh)
	print('xdx\tcount\tavg: ', len(z_xdx), '\t', av_xdx)
	print('intrans\tcount\tavg: ', len(z_intrans), '\t', av_intrans)
	print('trans\tcount\tavg: ', len(z_trans), '\t', av_trans)
	print('ditrans\tcount\tavg: ', len(z_ditrans), '\t', av_ditrans)
	print('targ\tcount\tavg: ', len(z_targ), '\t', av_targ)
	print('untarg\tcount\tavg: ', len(z_untarg), '\t', av_untarg)
	print('prim\tcount\tavg: ', len(z_prim), '\t', av_prim)
	print('mix\tcount\tavg: ', len(z_mix), '\t', av_mix)
	print('bert\tcount\tavg: ', len(z_bert), '\t', av_bert)
	return samp_avgs


def write_output(rs):
	outnm =('/Users/leviking/Documents/dissertation/SAILS/stats/'+
			'param_avg_response_scores-VS-N70.csv')
	thisfile=open(outnm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


my_exps = ['transitivity', 'targeting', 'primacy']
paramd = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["r1-", "r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}
labeld = {'T-': 'Targ', 'U-': 'Untarg', '-In-': 'Intrans', '-Tr-': 'Trans', '-Di-': 'Ditrans', '-gNSC-': 'Crowd', '-gNSF-': 'Fam', 'r1-': 'Prim', 'r2-': 'Mix'}

my_samples = ['F14', 'N14', 'N50']
def main():
	index_col = ['param', 'Intrans', 'Trans', 'Ditrans', 'Targ', 'Untarg', 'Prim',
				 'Mixed', 'ldh', 'xdh', 'xdx', 'BERT']
	sample_columns = [index_col]
	for my_sample in my_samples:
		my_input_dir = ("/Users/leviking/Documents/dissertation/SAILS/"+
						"test_data/scored/"+my_sample+"-VS-N70-BERT/")
		my_inputs = get_input_file_names(my_input_dir)
		sample_column = get_param_avg_scores(my_input_dir, my_inputs)
		sample_column.insert(0, my_sample)
		sample_columns.append(sample_column)
	all_rows = zip(*sample_columns)
	write_output(all_rows)
	


if __name__ == "__main__":
    main()
