#!/usr/bin/env python


## 2020/07/28. Branched from get_all_spearman_correlations.py
## This script runs t-test / wilcox for each of the five binary annotations


import sys, math, csv
from os import walk
from scipy import stats
# from scipy.stats import spearmanr
import numpy as np
import pandas as pd
import random


test_sample = "N70"
# sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'+test_sample+'/')
sourcedir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/N70/')
outdir=('/Users/leviking/Documents/dissertation/SAILS/stats/'+test_sample+'/significance/')
inicks = {'I01': 'i01_in_dance', 'I02': 'i02_tr_eat', 'I03': 'i03_di_deliver', 'I04': 'i04_in_wake', 'I05': 'i05_di_teach', 'I06': 'i06_tr_carry', 'I07': 'i07_in_fly', 'I08': 'i08_di_serve', 'I09': 'i09_tr_ride', 'I10': 'i10_in_cry', 'I11': 'i11_di_ask', 'I12': 'i12_tr_cut', 'I13': 'i13_in_swim', 'I14': 'i14_di_sell', 'I15': 'i15_tr_plant', 'I16': 'i16_tr_catch', 'I17': 'i17_di_feed', 'I18': 'i18_in_cough', 'I19': 'i19_tr_photo', 'I20': 'i20_in_laugh', 'I21': 'i21_di_throw', 'I22': 'i22_tr_forecast', 'I23': 'i23_di_inject', 'I24': 'i24_in_sleep', 'I25': 'i25_tr_chase', 'I26': 'i26_di_readto', 'I27': 'i27_in_sing', 'I28': 'i28_di_givedirection', 'I29': 'i29_tr_cuddle', 'I30': 'i30_in_run'}
depforms = ["ldh", "xdh"]


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if ".csv" in dn]
	docnames.sort()
	return docnames


def get_significance(my_feat, model_name, my_nick, my_df):
	my_dp = model_name[2:5]
	feat_col = my_df[my_feat]
	depform_col = my_df[my_dp+"_TC"]
	feat_zeroes = pd.Series(my_df.loc[my_df[my_feat] == 0][my_dp+"_TC"])
	feat_ones = pd.Series(my_df.loc[my_df[my_feat] == 1][my_dp+"_TC"])
	t_stat, p_val =  stats.ttest_ind(feat_zeroes, feat_ones, equal_var=False)
	my_sig_row = [t_stat, p_val]
	my_header = [model_name, "p_"+model_name]
	sig_df = pd.DataFrame([my_sig_row], index = [my_nick], columns = my_header)
	# print(sig_df)
	# print("\n\n\n")
	return sig_df


def process_one_file(inf):
	source_df = pd.read_csv(sourcedir+inf, index_col=0)
	inf_tags = inf.split("-")
	item = inf_tags[0]
	targeting = item[-1]
	item = item[:-1]
	inick = inicks[item]
	r1r2 = inf_tags[2]
	inf_df = 0
	for dp in depforms:
		model_name = targeting+"_"+dp+"_"+r1r2
		dp_df = get_significance("Core", model_name, inick, source_df)
		if type(inf_df) == int:
			inf_df = dp_df
		else:
			inf_df = pd.concat([inf_df, dp_df], axis=1, sort=False)
	return item, inf_df




def main():
	input_files = get_infile_names(sourcedir)  ## e.g. I23T-gNSC-r1-Di-N50-VS-N70.csv
	current = "I00"
	for inpf in input_files:
		itm, inpf_df = process_one_file(inpf)
		if current == "I00":
			item_row_df = inpf_df
			current = itm
		elif itm == current:
			item_row_df = pd.concat([item_row_df, inpf_df], axis=1, sort=False)
			current = itm
		else:
			try:  ## this will fail on first pass -- OK
				mega_df = mega_df.append(item_row_df)
			except:
				mega_df = item_row_df
			item_row_df = inpf_df
			current = itm
	mega_df = mega_df.append(item_row_df)
	print(mega_df)
	print("\n\n\n")


if __name__ == "__main__":
    main()
