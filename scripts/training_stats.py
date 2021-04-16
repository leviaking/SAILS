#!/usr/bin/env python


## 2021/04/12. Adapted from thesis_spearman_stats.py
## For a given sample size that we've used (so far: N14, N50, F14), this finds all the training files and generates response length, word TTR and termrep TTR descriptive stats for the various variables/parameter settings. Note that the termnorm (aka weighting) parameter does not apply here -- we do not operate on any kind of special weighted version of the training files, only the basic versions.


import sys, math, csv, pandas
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
pandas.options.display.float_format = '{:.3f}'.format



def get_training_file_names(tr_dir): 
	training_file_names = []
	for (dirpath, dirnames, filenames) in walk(tr_dir):
		training_file_names.extend(filenames)
		break
	training_file_names = [j for j in training_file_names if j.endswith(".csv")]
	training_file_names.sort()
	return training_file_names


def get_training_dfs(tr_dir, tr_fns):
	tr_dict = {}
	for trf in tr_fns:
		td = pandas.read_csv(tr_dir+trf, index_col=0, usecols=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
		tr_dict[trf] = td
	return tr_dict


def string_list_to_real_list(pylist):
	pylist = pylist[1:-1]
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%")
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist


def get_length_stats(tr_samp, train_fns, tdict, param_dict):
	alldf = pandas.DataFrame([])
	mycols = []
	for exp in my_exps:
		settings = param_dict[exp]
		for sg in settings:
			mycols.append(sg)
			sgdf = pandas.DataFrame([], columns=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
			for tf in train_fns:
				if sg in tf:
					tfd = tdict[tf]
					if sgdf.empty:
						sgdf = tfd
					else:
						sgdf = sgdf.append(tfd)
			sg_sents = list(sgdf["Response"])
			sg_sents = [g.replace(".", " ") for g in sg_sents]
			sg_sents = [g.replace(",", " ") for g in sg_sents]
			sg_sents = [g.replace(";", " ") for g in sg_sents]
			sg_sents = [g.replace(":", " ") for g in sg_sents]
			sg_sents = [g.replace("!", " ") for g in sg_sents]
			sg_sents = [g.replace("?", " ") for g in sg_sents]
			sg_sents = [g.replace("  ", " ") for g in sg_sents]
			sg_sents = [g.replace("  ", " ") for g in sg_sents]
			sg_sents = [g.replace("  ", " ") for g in sg_sents]
			sg_sents = [g.replace("  ", " ") for g in sg_sents]
			sg_sents = [g.strip() for g in sg_sents]
			sg_lengths = []
			sg_sorter = []
			for gx in sg_sents:
				sglen = len(gx.split(" "))
				sg_lengths.append(sglen)
				sg_sorter.append((sglen, gx))
			sg_sorter.sort(reverse=True)
			lendf = pandas.DataFrame(sg_lengths, columns=["lengths"])
			# print("\n\n\n\n\n\n\n\n\n\n\n\nSETTINGS LEVEL STATS for "+exp+sg+":")
			lenstats = lendf.describe(percentiles=[.5])
			lenstats.columns = [sg]
			if alldf.empty:
				alldf = pandas.DataFrame(lenstats)
			else:
				alldf = pandas.concat([alldf, lenstats], axis=1)
	print(alldf)
	alldf.to_csv(stats_dir+tr_samp+'_length_stats.csv', encoding='utf-8')


### for each FILE, get 1 TTR; based on the sg, we add TTR to the appropriate list;
### then we run DataFrame.describe() on the lists...

def get_word_ttrs(tr_samp, train_fns, tdict, param_dict):
	alldf = pandas.DataFrame([])
	mycols = []
	for exp in my_exps:
		settings = param_dict[exp]
		for sg in settings:
			mycols.append(sg)
			# sgdf = pandas.DataFrame([], columns=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
			# sgdf = pandas.DataFrame([], columns=['Source', 'Word_TTR'])
			sgttrs = []
			for tf in train_fns:
				tfd = tdict[tf]
				tsents = list(tfd["Response"])
				tsents = [g.lower() for g in tsents]
				tsents = [g.replace(".", " ") for g in tsents]
				tsents = [g.replace(",", " ") for g in tsents]
				tsents = [g.replace(";", " ") for g in tsents]
				tsents = [g.replace(":", " ") for g in tsents]
				tsents = [g.replace("!", " ") for g in tsents]
				tsents = [g.replace("?", " ") for g in tsents]
				tsents = [g.replace("  ", " ") for g in tsents]
				tsents = [g.replace("  ", " ") for g in tsents]
				tsents = [g.replace("  ", " ") for g in tsents]
				tsents = [g.replace("  ", " ") for g in tsents]
				tsents = [g.strip() for g in tsents]
				tstring = " ".join(tsents)
				ttokens = tstring.split(" ")
				ttypes = list(set(ttokens))
				t_ttr = float(len(ttypes)/len(ttokens))
				# print(tf, "\n", tstring, "\n", t_ttr, "\n\n\n\n\n\n")
				if sg in tf:
					sgttrs.append([tf, t_ttr])
				else:
					pass
			print("\n\n\n", sg)
			sgdf = pandas.DataFrame(sgttrs, columns=['Source', 'Word_TTR'])
			print(sgdf)
			ttrdf = pandas.DataFrame(sgdf, columns=["Word_TTR"])
			# print("\n\n\n\n\n\n\n\n\n\n\n\nSETTINGS LEVEL STATS for "+exp+sg+":")
			ttrstats = ttrdf.describe(percentiles=[.5])
			ttrstats.columns = [sg]
			if alldf.empty:
				alldf = pandas.DataFrame(ttrstats)
			else:
				alldf = pandas.concat([alldf, ttrstats], axis=1)
	print(alldf)
	alldf.to_csv(stats_dir+tr_samp+'_word_ttr_stats.csv', encoding='utf-8')


def get_termrep_ttrs(tr_samp, train_fns, t_dict):
	exp = 'termrep'
	settings = ['ldh', 'xdh', 'xdx']
	# settings = ['ldh']
	tfns_cute = [y.replace(".csv", "") for y in train_fns]
	termrep_ttrs = {}
	statsdf = pandas.DataFrame([])
	for setting in settings:
		setting_ttrs = []
		for tf in train_fns:
			tfd = t_dict[tf]  ## training file dataframe
			setting_col = tfd[setting]
			setting_tokens = [string_list_to_real_list(y) for y in setting_col]
			setting_tokens = [item for sublist in setting_tokens for item in sublist]
			setting_types = list(set(setting_tokens))
			setting_ttr = float(len(setting_types)/len(setting_tokens))
			setting_ttrs.append(setting_ttr)
		termrep_ttrs[setting] = setting_ttrs
		setting_ttrs_df = pandas.DataFrame(setting_ttrs, columns=[setting])
		ttrstats = setting_ttrs_df.describe(percentiles=[.5])
		ttrstats.columns = [setting]

		if statsdf.empty:
			statsdf = pandas.DataFrame(ttrstats)
		else:
			statsdf = pandas.concat([statsdf, ttrstats], axis=1)
	print(statsdf)
	statsdf.to_csv(stats_dir+tr_samp+'_termrep_ttr_stats.csv', encoding='utf-8')
	termrepdf = pandas.DataFrame(termrep_ttrs, index=tfns_cute)
	termrepdf.to_csv(stats_dir+tr_samp+'_termrep_ttrs.csv', encoding='utf-8')


my_exps = ['transitivity', 'targeting', 'primacy']
## Use this param_dict for any crowdsourced training runs
param_dict_crowd = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}
## Use this param_dict for any familiar training runs
param_dict_fam = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}


stats_dir="/Users/leviking/Documents/dissertation/SAILS/stats/"


def main():
	for train_sample in ["N14", "N50", "F14"]:
		# print(train_sample)
		if train_sample.startswith("N"):
			paramd = param_dict_crowd
		elif train_sample.startswith("F"):
			paramd = param_dict_fam
		train_dir = ('/Users/leviking/Documents/dissertation/SAILS/training_data/'
					 +train_sample+'/')
		train_file_names = get_training_file_names(train_dir)
		train_dict = get_training_dfs(train_dir, train_file_names)
		get_length_stats(train_sample, train_file_names, train_dict, paramd)
		get_word_ttrs(train_sample, train_file_names, train_dict, paramd)
		get_termrep_ttrs(train_sample, train_file_names, train_dict)





if __name__ == "__main__":
    main()