#!/usr/bin/env python


## 2021/03/02. Adapted from thesis_bert_spearman_stats.py
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
	"""Source	BERT_spear	BERT_p"""
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
	for rw in rws:
		srcn = rw[0]
		bert_k = srcn.replace("-r1-", "-r1-bert-")
		bert_k = bert_k.replace("-r2-", "-r2-bert-")
		sources.append(bert_k)
		sdict[bert_k] = [float(rw[1]), float(rw[2])]
	return sources, sdict


# my_exps = [['transitivity'], ['targeting'], ['primacy'], ['termrep'], ['transitivity', 'targeting'], ['transitivity', 'primacy'], ['transitivity', 'termrep'], ['targeting', 'primacy'], ['targeting', 'termrep'], ['primacy', 'termrep']]
## 20210225: switch to above version of my_exps after adding the logic
my_exps = [['transitivity'], ['targeting'], ['primacy'], ['termrep']]
param_dict = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['bert']}


def from_experiment_get_stats_csvs(wd, exp, all_sources, sd, trr, tss):
	# print(wd)
	tag = trr+"-VS-"+tss
	print(tag)
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
				if setting == 'bert':
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
				elif setting in sr:
					sr_spmn = sd[sr][0]
					sr_pval = sd[sr][1]
					ps_rows.append([sr, sr_spmn, sr_pval])
				else:
					pass
			ps_df = pandas.DataFrame(ps_rows)
			# print(ps_df)
			ps_sp_descriptive = ps_df[1].describe()
			# print(ps_sp_descriptive)
			ps_pv_descriptive = ps_df[2].describe()
			param_header.append(ps_name)
			param_stats.append(ps_sp_descriptive)
			# print(ps_name)
			ps_df.to_csv(wd+"bert-"+ps_name+'_spearman-'+tag+'.csv',
						 encoding='utf-8', index=False, header=x_head)
			ps_sp_descriptive.to_csv(wd+"bert-"+ps_name+'_spearman_stats-'+tag+
									 '.csv', encoding='utf-8', header=['spearman'])
			ps_pv_descriptive.to_csv(wd+"bert-"+ps_name+'_sp_pval_stats-'+tag+
									 '.csv', encoding='utf-8', header=['p_value'])
		# param_col_zero = ['null', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
		p_descriptive = pandas.concat([pd for pd in param_stats], axis=1)
		p_descriptive.to_csv(wd+"bert-"+param+'_spearman_stats-'+tag+'.csv',
							 encoding='utf-8', header=param_header)


def main():
	train_sample = "N14"
	test_sample = "N70"
	working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/"+
				 train_sample+'-VS-'+test_sample+'/')
	all_spearman_file = "bert_spearman_"+train_sample+"-VS-"+test_sample+".csv"
	oldheader, all_spearman_rows = get_source_rows(working_dir+all_spearman_file)
	# oldheader = ["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]
	all_sources, s_dict = get_spearman_dict(all_spearman_rows)  ## ['I01T-gNSC-r1-In-N50-VS-N70', ...], [ldh_sd, xdh_sd, xdx_sd]
	for exp in my_exps:
		from_experiment_get_stats_csvs(working_dir, exp, all_sources, s_dict,
									   train_sample, test_sample)

if __name__ == "__main__":
    main()
