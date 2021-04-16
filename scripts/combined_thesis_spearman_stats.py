#!/usr/bin/env python

### BE SURE TO SET *BOTH* VARIABLES BELOW: train_sample AND weighted

## 2021/04/01. Adapted from thesis_spearman_stats.py
## operates on, e.g.: combined_spearman_N14-VS-N70.csv
## or generally: combined_spearman_<XYZ>-VS-N70.csv , where XYZ is currently
## either: F14 (Familiar), N14, or N50.
## the point of this one is to get descriptive stats covering all 360 system
## scores and descriptive stats covering all 120 BERT scores. I haven't needed
## this yet but now I'm making tables for the weighted (termnorm) experiments
## and those do need to scope over all 360 (or 120).


import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
import pandas
pandas.options.display.float_format = '{:.10f}'.format


def get_source_rows(tdf):
	## header row:
	"""Source	ldh_spear	ldh_p	xdh_spear	xdh_p	xdx_spear	xdx_p	BERT_spear	BERT_p"""
	everything=[]
	tdoc=open(tdf, 'r')
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
	sources = []
	sdict = {}
	# ldh_sd = {}
	# xdh_sd = {}
	# xdx_sd = {}
	for rw in rws:
		srcn = rw[0]
		ldh_k = srcn.replace("-r1-", "-r1-s_ldh-")
		ldh_k = ldh_k.replace("-r2-", "-r2-s_ldh-")
		sources.append(ldh_k)
		xdh_k = srcn.replace("-r1-", "-r1-s_xdh-")
		xdh_k = xdh_k.replace("-r2-", "-r2-s_xdh-")
		sources.append(xdh_k)
		xdx_k = srcn.replace("-r1-", "-r1-s_xdx-")
		xdx_k = xdx_k.replace("-r2-", "-r2-s_xdx-")
		sources.append(xdx_k)
		bert_k = srcn.replace("-r1-", "-r1-bert-")
		bert_k = bert_k.replace("-r2-", "-r2-bert-")
		sources.append(bert_k)
		sdict[ldh_k] = [float(rw[1]), float(rw[2])]
		sdict[xdh_k] = [float(rw[3]), float(rw[4])]
		sdict[xdx_k] = [float(rw[5]), float(rw[6])]
		sdict[bert_k] = [float(rw[7]), float(rw[8])]
	return sources, sdict


## the original run:
# my_exps = [['transitivity'], ['targeting'], ['primacy'], ['termrep']]
## the termnorm run (covers ALL configurations (once for system, once for bert)):
my_exps = [['termnorm']]
## Use this param_dict for any crowdsourced training runs
param_dict = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['ldh', 'xdh', 'xdx'], 'termnorm': ["-s_", "-bert-"]}
# # Use this param_dict for any familiar training runs
# param_dict = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r2-"], 'termrep': ['ldh', 'xdh', 'xdx'], 'termnorm': ["-s_", "-bert-"]}


def from_experiment_get_stats_csvs_unweighted(wd, exp, all_sources, sd, trr, tss):
	tag = trr+"-VS-"+tss
	for param in exp:
		settings = param_dict[param]
		x_head = ['source', 'spearman', 'p_val']
		param_header = []
		param_stats = []
		for setting in settings:
			setting_name = ''.join([i for i in setting if i.isalnum()])
			ps_name = param+"_"+setting_name
			ps_name = ps_name.replace("_s", "_sys")
			ps_rows = []
			for sr in all_sources:  ## e.g. 'I01T-gNSC-r1-In-N50-VS-N70'
				if setting in sr:
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
			ps_df = pandas.DataFrame(ps_rows)
			ps_sp_descriptive = ps_df[1].describe()
			ps_pv_descriptive = ps_df[2].describe()
			param_header.append(ps_name)
			param_stats.append(ps_sp_descriptive)
			ps_df.to_csv(wd+ps_name+'_spearman-'+tag+'.csv', encoding='utf-8',
						 index=False, header=x_head)
			ps_sp_descriptive.to_csv(wd+ps_name+'_spearman_stats-'+tag+'.csv',
									 encoding='utf-8', header=['spearman'])
			ps_pv_descriptive.to_csv(wd+ps_name+'_sp_pval_stats-'+tag+'.csv', encoding='utf-8', header=['p_value'])
		# param_col_zero = ['null', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
		p_descriptive = pandas.concat([pd for pd in param_stats], axis=1)
		p_descriptive.to_csv(wd+param+'_spearman_stats-'+tag+'.csv', encoding='utf-8', header=param_header)


def from_experiment_get_stats_csvs_weighted(wd, exp, all_sources, sd, trr, tss):
	tag = trr+"-VS-"+tss
	for param in exp:
		settings = param_dict[param]
		x_head = ['source', 'spearman', 'p_val']
		param_header = []
		param_stats = []
		for setting in settings:
			setting_name = ''.join([i for i in setting if i.isalnum()])
			ps_name = param+"_"+setting_name
			ps_name = ps_name.replace("_s", "_sys")
			ps_rows = []
			for sr in all_sources:  ## e.g. 'I01T-gNSC-r1-In-N50-VS-N70'
				if setting in sr:
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
			ps_df = pandas.DataFrame(ps_rows)
			ps_sp_descriptive = ps_df[1].describe()
			ps_pv_descriptive = ps_df[2].describe()
			param_header.append(ps_name)
			param_stats.append(ps_sp_descriptive)
			ps_df.to_csv(wd+ps_name+'_spearman-'+tag+'-W.csv', encoding='utf-8',
						 index=False, header=x_head)
			ps_sp_descriptive.to_csv(wd+ps_name+'_spearman_stats-'+tag+'-W.csv',
									 encoding='utf-8', header=['spearman'])
			ps_pv_descriptive.to_csv(wd+ps_name+'_sp_pval_stats-'+tag+'-W.csv', encoding='utf-8', header=['p_value'])
		# param_col_zero = ['null', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
		p_descriptive = pandas.concat([pd for pd in param_stats], axis=1)
		p_descriptive.to_csv(wd+param+'_spearman_stats-'+tag+'-W.csv', encoding='utf-8', header=param_header)


def main():
	train_sample = "N14"
	weighted = "no"
	test_sample = "N70"
	## WEIGHTED version
	if weighted == "yes":
		working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/"+
					 train_sample+'-VS-'+test_sample+'-W/')
		comb_spearman_file = "combined_spearman_"+train_sample+"-VS-"+test_sample+"-W.csv"
	else:
	## UNWEIGHTED version
		working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/"+
					 train_sample+'-VS-'+test_sample+'/')
		comb_spearman_file = "combined_spearman_"+train_sample+"-VS-"+test_sample+".csv"
	oldheader, comb_spearman_rows = get_source_rows(working_dir+comb_spearman_file)
	# oldheader = ["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]
	comb_sources, s_dict = get_spearman_dict(comb_spearman_rows)  ## ['I01T-gNSC-r1-ldh-In-N50-VS-N70', ...], [ldh_sd, xdh_sd, xdx_sd]
	for exp in my_exps:
		if weighted == "yes":
			from_experiment_get_stats_csvs_weighted(working_dir, exp, comb_sources,
													s_dict, train_sample, test_sample)
		else:
			from_experiment_get_stats_csvs_unweighted(working_dir, exp, comb_sources,
													  s_dict,train_sample, test_sample)


if __name__ == "__main__":
    main()
