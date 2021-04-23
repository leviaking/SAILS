#!/usr/bin/env python


## 2021/04/22. Adapted from training_stats.py
## For the specified (and extant) test sample(s), this script churns through the (60) test files and generates response length, word TTR and termrep TTR descriptive stats.


import sys, math, csv, pandas
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
pandas.options.display.float_format = '{:.3f}'.format



def get_test_file_names(ts_dir): 
	ts_file_names = []
	for (dirpath, dirnames, filenames) in walk(ts_dir):
		ts_file_names.extend(filenames)
		break
	ts_file_names = [j for j in ts_file_names if j.endswith(".csv")]
	ts_file_names.sort()
	return ts_file_names


def get_test_dfs(ts_dir, ts_fns):
	ts_dict = {}
	for tsf in ts_fns:
		td = pandas.read_csv(ts_dir+tsf, index_col=0, usecols=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
		ts_dict[tsf] = td
	return ts_dict


def string_list_to_real_list(pylist):
	pylist = pylist[1:-1]
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%")
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist


def quick_clean_response_list(resp_l):
	resp_l = [g.replace(".", " ") for g in resp_l]
	resp_l = [g.replace(",", " ") for g in resp_l]
	resp_l = [g.replace(";", " ") for g in resp_l]
	resp_l = [g.replace(":", " ") for g in resp_l]
	resp_l = [g.replace("!", " ") for g in resp_l]
	resp_l = [g.replace("?", " ") for g in resp_l]
	resp_l = [g.replace("  ", " ") for g in resp_l]
	resp_l = [g.replace("  ", " ") for g in resp_l]
	resp_l = [g.replace("  ", " ") for g in resp_l]
	resp_l = [g.replace("  ", " ") for g in resp_l]
	resp_l = [g.strip() for g in resp_l]
	return resp_l


## words per response
def get_length_stats(ts_samp, ts_fns, tdict, param_dict):
	##this is ugly but it's okay for now... I'm iterating through more than would be necessary if this were handled more elegantly...
	tf_lengths = []
	tfns_cute = []
	for tfx in ts_fns:
		tfx_cute = tfx.replace(".csv", "")
		tfns_cute.append(tfx_cute)
		tfxd = tdict[tfx]
		tfx_responses = list(tfxd["Response"])
		tfx_responses = quick_clean_response_list(tfx_responses)
		tfx_lengths = [len(h.split(" ")) for h in tfx_responses]
		tfx_avg_length = float(sum(tfx_lengths)/len(tfx_lengths))
		# tf_lengths.append([tfx_cute, tfx_avg_length])
		tf_lengths.append(tfx_avg_length)
	tf_lengths_dict = {}
	tf_lengths_dict["AvgWdsPerResp"] = tf_lengths
	tf_lengths_df = pandas.DataFrame(tf_lengths_dict, index=tfns_cute)
	tf_lengths_df.to_csv(stats_dir+"NNS-"+ts_samp+'_lengths.csv', encoding='utf-8')
	## this is where it starts iterating again...
	alldf = pandas.DataFrame([])
	mycols = []
	for exp in my_exps:
		settings = param_dict[exp]
		for sg in settings:
			mycols.append(sg)
			sgdf = pandas.DataFrame([], columns=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
			for tf in ts_fns:
				if sg in tf:
					tfd = tdict[tf]
					if sgdf.empty:
						sgdf = tfd
					else:
						sgdf = sgdf.append(tfd)
			sg_sents = list(sgdf["Response"])
			sg_sents = quick_clean_response_list(sg_sents)
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
	# print(alldf)
	alldf.to_csv(stats_dir+"NNS-"+ts_samp+'_length_stats.csv', encoding='utf-8')


### for each training FILE (NS model), get 1 word TTR; based on the setting,
## we add TTR to the appropriate list; then we run DataFrame.describe() on the lists...
def get_word_ttrs(ts_samp, ts_fns, tdict, param_dict):
	# tfns_cute = [y.replace(".csv", "") for y in ts_fns]
	describe_df = pandas.DataFrame([])
	# model_ttrs_dict = {}
	model_ttrs = []
	tfns_cute = []
	mycols = []
	for exp in my_exps:
		settings = param_dict[exp]
		for sg in settings:
			mycols.append(sg)
			# sgdf = pandas.DataFrame([], columns=['ResponseID', 'Response', 'ldh', 'xdh', 'xdx'])
			# sgdf = pandas.DataFrame([], columns=['Source', 'Word_TTR'])
			sgttrs = []
			for tf in ts_fns:
				tfd = tdict[tf]
				tsents = list(tfd["Response"])
				tsents = quick_clean_response_list(tsents)
				tstring = " ".join(tsents)
				ttokens = tstring.split(" ")
				ttypes = list(set(ttokens))
				t_ttr = float(len(ttypes)/len(ttokens))
				tcute = tf.replace(".csv", "")
				if tcute not in tfns_cute:
					model_ttrs.append(t_ttr)
					tfns_cute.append(tcute)
				else:
					pass
				# model_ttrs_dict[tf] = t_ttr
				# print(tf, "\n", tstring, "\n", t_ttr, "\n\n\n\n\n\n")
				if sg in tf:
					sgttrs.append([tf, t_ttr])
				else:
					pass
			# print("\n\n\n", sg)
			sgdf = pandas.DataFrame(sgttrs, columns=['Source', 'Word_TTR'])
			# print(sgdf)
			ttrdf = pandas.DataFrame(sgdf, columns=["Word_TTR"])
			# print("\n\n\n\n\n\n\n\n\n\n\n\nSETTINGS LEVEL STATS for "+exp+sg+":")
			ttrstats = ttrdf.describe(percentiles=[.5])
			ttrstats.columns = [sg]
			if describe_df.empty:
				describe_df = pandas.DataFrame(ttrstats)
			else:
				describe_df = pandas.concat([describe_df, ttrstats], axis=1)
	model_dict = {}
	model_dict["Word_TTR"] = model_ttrs
	model_ttrs_df = pandas.DataFrame(model_dict, index=tfns_cute)
	model_ttrs_df.to_csv(stats_dir+"NNS-"+ts_samp+'_word_ttrs.csv', encoding='utf-8')
	describe_df.to_csv(stats_dir+"NNS-"+ts_samp+'_word_ttr_stats.csv', encoding='utf-8')


## for each test file, get TTRs (ldh, xdh, xdx); based on the setting,
## we add TTR to the appropriate list; then we run DataFrame.describe() on the lists;
## this function currently writes out a descriptive stats csv for each model size
## showing the stats for each isolated parameter setting; it aso writes out a 
def get_termrep_ttrs(ts_samp, ts_fns, t_dict):
	exp = 'termrep'
	settings = ['ldh', 'xdh', 'xdx']
	# settings = ['ldh']
	tfns_cute = [y.replace(".csv", "") for y in ts_fns]
	termrep_ttrs = {}
	statsdf = pandas.DataFrame([])
	for setting in settings:
		setting_ttrs = []
		for tf in ts_fns:
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
		ttrstats.columns = [setting+"_ttr"]

		if statsdf.empty:
			statsdf = pandas.DataFrame(ttrstats)
		else:
			statsdf = pandas.concat([statsdf, ttrstats], axis=1)
	# print(statsdf)
	statsdf.to_csv(stats_dir+"NNS-"+ts_samp+'_termrep_ttr_stats.csv', encoding='utf-8')
	termrepdf = pandas.DataFrame(termrep_ttrs, index=tfns_cute)
	termrepdf.to_csv(stats_dir+"NNS-"+ts_samp+'_termrep_ttrs.csv', encoding='utf-8')


my_exps = ['transitivity', 'targeting']
## Use this param_dict for any crowdsourced training runs
paramd = {'transitivity': ["-In-", "-Tr-", "-Di-"], 'targeting': ['T-', 'U-'], 'familiarity': ["-gNSC-", "-gNSF-"], 'primacy': ["-r1-", "-r2-"], 'termrep': ['ldh', 'xdh', 'xdx']}
# transdict = {
# 	"-In-" : ["I01", "I04", "I07", "I10", "I13", "I18", "I20", "I24", "I27", "I30"],
# 	"-Tr-" : ["I02", "I06", "I09", "I12", "I15", "I16", "I19", "I22", "I25", "I29"],
# 	"-Di-" : ["I03", "I05", "I08", "I11", "I14", "I17", "I21", "I23", "I26", "I28"]
# 	}

stats_dir="/Users/leviking/Documents/dissertation/SAILS/stats/"


def main():
	for test_sample in ["N70"]:
		# print(train_sample)
		test_dir = ('/Users/leviking/Documents/dissertation/SAILS/test_data/'
					 +test_sample+'/')
		test_file_names = get_test_file_names(test_dir)
		test_dict = get_test_dfs(test_dir, test_file_names)
		get_length_stats(test_sample, test_file_names, test_dict, paramd)
		get_word_ttrs(test_sample, test_file_names, test_dict, paramd)
		get_termrep_ttrs(test_sample, test_file_names, test_dict)





if __name__ == "__main__":
    main()
