#!/usr/bin/env python


## 2021/04/27. Adapted from training_stats.py
## totally incomplete now...

## 2021/04/12. Adapted from thesis_spearman_stats.py
## For a given sample size that we've used (so far: N14, N50, F14), this finds all the training files and generates response length, word TTR and termrep TTR descriptive stats for the various variables/parameter settings. Note that the termnorm (aka weighting) parameter does not apply here -- we do not operate on any kind of special weighted version of the training files, only the basic versions.

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


def get_input_dfs(input_dir, input_fns):
	input_dict = {}
	# mycols = ['ResponseID', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif', 'AnnoRank', 'ldh TC', 'xdh TC', 'xdx TC', 'BERT_rank']
	for ipf in input_fns:
		ipdf = pandas.read_csv(input_dir+ipf, index_col='ResponseID', usecols=['ResponseID', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif', 'AnnoRank', 'ldh TC', 'xdh TC', 'xdx TC', 'BERT_rank'])
		# ldh_tc = list(ipdf_raw['ldh TC'])
		# print(type(ldh_tc))
		ldh_ranks = list(rankdata(list(ipdf['ldh TC'])).astype(float))
		xdh_ranks = list(rankdata(list(ipdf['xdh TC'])).astype(float))
		xdx_ranks = list(rankdata(list(ipdf['xdx TC'])).astype(float))
		# print(ldh_ranks)
		ipdf["ldh_rank"] = ldh_ranks
		ipdf["xdh_rank"] = xdh_ranks
		ipdf["xdx_rank"] = xdx_ranks
		ipdf = ipdf.drop(columns=['ldh TC', 'xdh TC', 'xdx TC'])
		input_dict[ipf] = ipdf
	return input_dict


def for_rank_df_get_avg_precisions(input_fn, rank_df):
	feats = ['Core', 'Answer', 'Gramm', 'Interp', 'Verif']
	rankers = ['AnnoRank', 'ldh_rank', 'xdh_rank', 'xdx_rank', 'BERT_rank']
	source = input_fn.replace("-BERT.csv", "")
	new_ap_row = [source]
	for ft in feats:
		true_ft = np.array(rank_df[ft])
		for rk in rankers:
			# label = rk.replace("Rank", "")
			# label = label.replace("_rank", "")
			# label = ft+"_"+label+"_AP"
			rk_ft = np.array(rank_df[rk])
			rf_ft_ap = average_precision_score(true_ft, rk_ft)
			new_ap_row.append(rf_ft_ap)
	return new_ap_row


def write_output(rs, nm):
	outdir =('/Users/leviking/Documents/dissertation/SAILS/average_precision/')
	thisfile=open(outdir+nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()




def main():
	my_input_dir = ("/Users/leviking/Documents/dissertation/SAILS/test_data/"+
					"scored/N50-VS-N70-BERT/")
	# my_inputs = ["I01T-gNSC-vs_r1-In-N50-VS-N70-BERT.csv"]
	my_inputs = get_input_file_names(my_input_dir)
	my_input_df = get_input_dfs(my_input_dir, my_inputs)
	ap_header =['Source', 'Core_Anno_AP', 'Core_ldh_AP', 'Core_xdh_AP', 'Core_xdx_AP', 'Core_BERT_AP', 'Answer_Anno_AP', 'Answer_ldh_AP', 'Answer_xdh_AP', 'Answer_xdx_AP', 'Answer_BERT_AP', 'Gramm_Anno_AP', 'Gramm_ldh_AP', 'Gramm_xdh_AP', 'Gramm_xdx_AP', 'Gramm_BERT_AP', 'Interp_Anno_AP', 'Interp_ldh_AP', 'Interp_xdh_AP', 'Interp_xdx_AP', 'Interp_BERT_AP', 'Verif_Anno_AP', 'Verif_ldh_AP', 'Verif_xdh_AP', 'Verif_xdx_AP', 'Verif_BERT_AP']
	ap_csv = [ap_header]
	# ap_df = pandas.DataFrame(columns = ap_header)
	for mi in my_inputs:
		# print(mi)
		# print(my_input_df[mi])
		mi_ap_row = for_rank_df_get_avg_precisions(mi, my_input_df[mi])
		ap_csv.append(mi_ap_row)
	write_output(ap_csv, 'NS50-vs-NNS70-average_precision.csv')



if __name__ == "__main__":
    main()
