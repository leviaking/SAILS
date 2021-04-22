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
		ldh_k = srcn.replace("-r1-", "-r1-ldh-")
		ldh_k = ldh_k.replace("-r2-", "-r2-ldh-")
		sources.append(ldh_k)
		xdh_k = srcn.replace("-r1-", "-r1-xdh-")
		xdh_k = xdh_k.replace("-r2-", "-r2-xdh-")
		sources.append(xdh_k)
		xdx_k = srcn.replace("-r1-", "-r1-xdx-")
		xdx_k = xdx_k.replace("-r2-", "-r2-xdx-")
		sources.append(xdx_k)
		sdict[ldh_k] = [float(rw[1]), float(rw[2])]
		sdict[xdh_k] = [float(rw[3]), float(rw[4])]
		sdict[xdx_k] = [float(rw[5]), float(rw[6])]
	return sources, sdict


# my_exps = [['transitivity'], ['targeting'], ['primacy'], ['termrep'], ['transitivity', 'targeting'], ['transitivity', 'primacy'], ['transitivity', 'termrep'], ['targeting', 'primacy'], ['targeting', 'termrep'], ['primacy', 'termrep']]
## 20210225: switch to above version of my_exps after adding the logic
my_exps = [['transitivity'], ['targeting'], ['primacy'], ['termrep']]
## Use this param_dict for any crowdsourced training runs
param_dict = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}
## Use this param_dict for any familiar training runs
# param_dict = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}


def from_exp_get_stats_csvs_weighted(wd, exp, all_sources, sd, trr, tss):
	tag = trr+"-VS-"+tss
	for param in exp:
		# print(all_sources)
		# print("param: "+param)
		settings = param_dict[param]
		x_head = ['source', 'spearman', 'p_val']
		param_header = []
		param_stats = []
		for setting in settings:
			# print("setting a: "+setting)
			setting_name = ''.join([i for i in setting if i.isalnum()])
			# print("setting_name: "+setting_name)
			ps_name = param+"_"+setting_name
			ps_rows = []
			for sr in all_sources:  ## e.g. 'I01T-gNSC-r1-In-N50-VS-N70'
				# print("setting b: "+setting)
				# print("sr: "+sr)
				if setting in sr:
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
					# t_rep_rows = query_termrep_dicts(sr, sd)
					# for tr in t_rep_rows:
					# 	ps_rows.append(tr)
			ps_df = pandas.DataFrame(ps_rows)
			# print(ps_df)
			ps_sp_descriptive = ps_df[1].describe()
			# print(ps_sp_descriptive)
			ps_pv_descriptive = ps_df[2].describe()
			param_header.append(ps_name)
			param_stats.append(ps_sp_descriptive)
			# print(ps_name)
			ps_df.to_csv(wd+ps_name+'_spearman-'+tag+'-W.csv', encoding='utf-8',
						 index=False, header=x_head)
			ps_sp_descriptive.to_csv(wd+ps_name+'_spearman_stats-'+tag+'-W.csv',
									 encoding='utf-8', header=['spearman'])
			ps_pv_descriptive.to_csv(wd+ps_name+'_sp_pval_stats-'+tag+'-W.csv', encoding='utf-8', header=['p_value'])
		# param_col_zero = ['null', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
		p_descriptive = pandas.concat([pd for pd in param_stats], axis=1)
		p_descriptive.to_csv(wd+param+'_spearman_stats-'+tag+'-W.csv', encoding='utf-8', header=param_header)


def from_exp_get_stats_csvs_unweighted(wd, exp, all_sources, sd, trr, tss):
	tag = trr+"-VS-"+tss
	for param in exp:
		# print(all_sources)
		# print("param: "+param)
		settings = param_dict[param]
		x_head = ['source', 'spearman', 'p_val']
		param_header = []
		param_stats = []
		for setting in settings:
			# print("setting a: "+setting)
			setting_name = ''.join([i for i in setting if i.isalnum()])
			# print("setting_name: "+setting_name)
			ps_name = param+"_"+setting_name
			ps_rows = []
			for sr in all_sources:  ## e.g. 'I01T-gNSC-r1-In-N50-VS-N70'
				# print("setting b: "+setting)
				# print("sr: "+sr)
				if setting in sr:
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
					# t_rep_rows = query_termrep_dicts(sr, sd)
					# for tr in t_rep_rows:
					# 	ps_rows.append(tr)
			ps_df = pandas.DataFrame(ps_rows)
			# print(ps_df)
			ps_sp_descriptive = ps_df[1].describe()
			# print(ps_sp_descriptive)
			ps_pv_descriptive = ps_df[2].describe()
			param_header.append(ps_name)
			param_stats.append(ps_sp_descriptive)
			# print(ps_name)
			ps_df.to_csv(wd+ps_name+'_spearman-'+tag+'.csv', encoding='utf-8',
						 index=False, header=x_head)
			ps_sp_descriptive.to_csv(wd+ps_name+'_spearman_stats-'+tag+'.csv',
									 encoding='utf-8', header=['spearman'])
			ps_pv_descriptive.to_csv(wd+ps_name+'_sp_pval_stats-'+tag+'.csv', encoding='utf-8', header=['p_value'])
		# param_col_zero = ['null', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
		p_descriptive = pandas.concat([pd for pd in param_stats], axis=1)
		p_descriptive.to_csv(wd+param+'_spearman_stats-'+tag+'.csv', encoding='utf-8', header=param_header)


def main():
	train_sample = "N50"
	weighted = "no"
	test_sample = "N02"
	if weighted == "yes":
		working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/"+
					 train_sample+'-VS-'+test_sample+'-W/')
		all_spearman_file = "all_spearman_"+train_sample+"-VS-"+test_sample+"-W.csv"
	else:
		working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/"+
					 train_sample+'-VS-'+test_sample+'/')
		all_spearman_file = "all_spearman_"+train_sample+"-VS-"+test_sample+".csv"
	oldheader, all_spearman_rows = get_source_rows(working_dir+all_spearman_file)
	# oldheader = ["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]
	all_sources, s_dict = get_spearman_dict(all_spearman_rows)  ## ['I01T-gNSC-r1-In-N50-VS-N70', ...], [ldh_sd, xdh_sd, xdx_sd]
	for exp in my_exps:
		if weighted == "yes":
			from_exp_get_stats_csvs_weighted(working_dir, exp, all_sources, s_dict,
											 train_sample, test_sample)
		else:
			from_exp_get_stats_csvs_unweighted(working_dir, exp, all_sources, s_dict,
											 train_sample, test_sample)


if __name__ == "__main__":
    main()
