#!/usr/bin/env python


import sys, csv
from scipy.stats import rankdata
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch
import random


def get_rows_by_param_settings(ps, fd):
	psrows = []
	for s in ps:
		srows = []
		for model_row in fd:
			if s in model_row[0]:
				srows.append(list(model_row))
		psrows.append(srows)
	return psrows


def get_param_averages(ps, psrows):
	pavgs = []
	rowlength = len(psrows[0][0])
	for pgroup in psrows:
		pavg = []
		for i in range(1, rowlength):  ## skip 0 because that column contains model names
			isum = 0.0
			for prow in pgroup:
				isum += prow[i]
			iavg = isum/(len(pgroup))
			pavg.append(iavg)
		pavgs.append(pavg)
	return(pavgs)


def draw_cluster_from_matrix(mydir, myfn, mtx):
	cluster_labels = ['i01_in_dance', 'i02_tr_eat', 'i03_di_deliver', 'i04_in_wake', 'i05_di_teach', 'i06_tr_carry', 'i07_in_fly', 'i08_di_serve', 'i09_tr_ride', 'i10_in_cry', 'i11_di_ask', 'i12_tr_cut', 'i13_in_swim', 'i14_di_sell', 'i15_tr_plant', 'i16_tr_catch', 'i17_di_feed', 'i18_in_cough', 'i19_tr_photo', 'i20_in_laugh', 'i21_di_throw', 'i22_tr_forecast', 'i23_di_inject', 'i24_in_sleep', 'i25_tr_chase', 'i26_di_readto', 'i27_in_sing', 'i28_di_givedirection', 'i29_tr_cuddle', 'i30_in_run']  ## csv header row (minus first cell)
	plt.figure(figsize=(12,8))
	mtx_df = pd.DataFrame(mtx)
	mtx_df = mtx_df.T		## Transpose
	# print(mtx_df)
	mtx_dendrogram = sch.dendrogram(sch.linkage(mtx_df, method  = "ward"), orientation="left", leaf_font_size=8, labels=cluster_labels)
	plt.title(myfn)
	plt.xlabel('Items')
	plt.ylabel('Euclidean distances')
	# plt.show()
	plt.savefig(mydir+myfn+".png",  pad_inches=1.0)
	plt.clf()


def draw_all_single_model_clusters(mlabs, workdir, fulld):
	for mlab in mlabs:
		mlab_rows = get_rows_by_param_settings([mlab], fulld)
		mlab_avgs = get_param_averages([mlab], mlab_rows)  ## hacky -- single row doesn't need to be averaged, but does need formatting
		draw_cluster_from_matrix(workdir, "cluster_"+mlab, mlab_avgs)

	
## 2020/10/12: Need to rethink the handling of clusters using *ranked* values... I've been ranking the items 1-30 according to their scores for a given model; instead, I should look at a given item and rank the models (1-12 I think). Ranking items by model isn't interesting -- an item with a weak spearman score will have a relatively weak spearman score across all models. Ranking models by item might be more interesting: Perhaps for certain models rank higher for certain types of items. I need a good pandas tutorial to teach me how to better handle dataframes. 

def main():
	working_dir = "/Users/leviking/Documents/dissertation/SAILS/stats/N70/"
	source_csv = working_dir+"all_spearman_N70-clustering_vectors.csv"
	dataset = pd.read_csv(source_csv)
	print(dataset)
	print(type(dataset))
	print("####################################")
	full_dataset = dataset.iloc[:].values
	print(full_dataset)
	print(type(full_dataset))
	model_labels = ['T_ldh_r1', 'T_xdh_r1', 'T_xdx_r1', 'T_ldh_r2', 'T_xdh_r2', 'T_xdx_r2', 'U_ldh_r1', 'U_xdh_r1', 'U_xdx_r1', 'U_ldh_r2', 'U_xdh_r2', 'U_xdx_r2']  ## column 0; currently unused here
	depform_settings = ["ldh", "xdh", "xdx"]
	r1r2_settings = ["r1", "r2"]
	TU_settings = ["T_", "U_"]

	depform_rows = get_rows_by_param_settings(depform_settings, full_dataset)  ## shouldn't need this with dataframes
	depform_avgs = get_param_averages(depform_settings, depform_rows)
	# depform_avgsranked = [list(rankdata(row).astype(float)) for row in depform_avgs]
	draw_cluster_from_matrix(working_dir, "cluster_depform_avgs", depform_avgs)
	# draw_cluster_from_matrix(working_dir, "cluster_depform_avgsranked", depform_avgsranked)

	# r1r2_rows = get_rows_by_param_settings(r1r2_settings, full_dataset)
	# r1r2_avgs = get_param_averages(r1r2_settings, r1r2_rows)
	# print(r1r2_avgs)
	# # r1r2_avgsranked = [list(rankdata(row).astype(float)) for row in r1r2_avgs]
	# draw_cluster_from_matrix(working_dir, "cluster_r1r2_avgs", r1r2_avgs)
	# # draw_cluster_from_matrix(working_dir, "cluster_r1r2_avgsranked", r1r2_avgsranked)
	# 
	# TU_rows = get_rows_by_param_settings(TU_settings, full_dataset)
	# TU_avgs = get_param_averages(TU_settings, TU_rows)
	# # TU_avgsranked = [list(rankdata(row).astype(float)) for row in TU_avgs]
	# draw_cluster_from_matrix(working_dir, "cluster_TU_avgs", TU_avgs)
	# # draw_cluster_from_matrix(working_dir, "cluster_TU_avgsranked", TU_avgsranked)
	# 
	# draw_all_single_model_clusters(model_labels, working_dir, full_dataset)

	# T_ldh_r1_rows = get_rows_by_param_settings(["T_ldh_r1"], full_dataset)
	# T_ldh_r1_avgs = get_param_averages(["T_ldh_r1"], T_ldh_r1_rows)  ## hacky -- single row doesn't need to be averaged, but does need formatting
	# draw_cluster_from_matrix(working_dir, "cluster_T_ldh_r1", T_ldh_r1_avgs)
	# # draw_cluster_from_matrix(working_dir, "cluster_T_ldh_r1_ranked", T_ldh_r1_ranked)
	
	

if __name__ == "__main__":
    main()
