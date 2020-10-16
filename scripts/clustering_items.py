#!/usr/bin/env python


import sys, csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch
import random


working_dir = "/Users/leviking/Documents/dissertation/SAILS/stats/N70/"


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


def draw_df_cluster(my_df, my_title):
	my_dendrogram = sch.dendrogram(sch.linkage(my_df, method  = "ward"), orientation="left", leaf_font_size=8, labels=my_df.index)
	# plt.tight_layout()
	plt.title(my_title)
	plt.xlabel('Items')
	plt.ylabel('Euclidean distances')
	plt.savefig(working_dir+"cluster_"+my_title+".png", bbox_inches = "tight", pad_inches=0.3)
	# plt.savefig(working_dir+"clustering_raw_model_scores_df"+".png",  pad_inches=1.0)
	plt.clf()
	my_df.to_csv(working_dir+my_title+".csv")


def draw_single_vector_clusters_from_df(my_df, my_title):
	for index in my_df:
		index_series = my_df[index]  ## series is single column vector from df
		index_df = index_series.to_frame()  ## convert back to df
		new_title = my_title+"_"+index
		draw_df_cluster(index_df, new_title)


def draw_item_avg_clusters(my_df, my_title):
	my_avgs_df = my_df.mean(axis=1).to_frame()
	my_avgs_df.rename(columns={0:my_title}, inplace = True)
	draw_df_cluster(my_avgs_df, my_title)


def draw_item_median_clusters(my_df, my_title):
	my_median_df = my_df.median(axis=1).to_frame()
	my_median_df.rename(columns={0:my_title}, inplace = True)
	draw_df_cluster(my_median_df, my_title)


def main():
	source_csv = working_dir+"all_spearman_N70-clustering_vectors.csv"
	full_df = pd.read_csv(source_csv, index_col=0)
	raw_df = full_df.T  ## Transpose
	ranked_models_by_item_df = raw_df.rank(axis=1)  ## models ranked by item
	ranked_items_by_model_df = raw_df.rank(axis=0)  ## items ranked by model
	plt.figure(figsize=(7,10))
	draw_df_cluster(raw_df, "raw_model_scores")
	draw_df_cluster(ranked_models_by_item_df, "ranked_model_scores")
	draw_single_vector_clusters_from_df(raw_df, "raw_model_scores")
	draw_single_vector_clusters_from_df(ranked_models_by_item_df, "ranked_model_scores")
	draw_item_avg_clusters(raw_df, "item_avg_raw_scores")
	draw_item_avg_clusters(ranked_items_by_model_df, "item_avg_ranked_scores")
	draw_item_median_clusters(raw_df, "item_median_raw_scores")
	draw_item_median_clusters(ranked_items_by_model_df, "item_median_ranked_scores")
	

	depform_settings = ["ldh", "xdh", "xdx"]
	r1r2_settings = ["r1", "r2"]
	TU_settings = ["T_", "U_"]


## TODO: 2020/10/15. Tomorrow, replicate the below using proper pandas as above.

	# # depform_rows = get_rows_by_param_settings(depform_settings, full_dataset)  ## shouldn't need this with dataframes
	# depform_avgs = get_param_averages(depform_settings, depform_rows)
	# # depform_avgsranked = [list(rankdata(row).astype(float)) for row in depform_avgs]
	# draw_cluster_from_matrix(working_dir, "cluster_depform_avgs", depform_avgs)
	# # draw_cluster_from_matrix(working_dir, "cluster_depform_avgsranked", depform_avgsranked)

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
	
	

if __name__ == "__main__":
    main()
