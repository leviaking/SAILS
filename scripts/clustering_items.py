#!/usr/bin/env python


import sys, csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch
import random


working_dir = "/Users/leviking/Documents/dissertation/SAILS/stats/N70/"


def draw_df_cluster(my_df, my_title):
	my_dendrogram = sch.dendrogram(sch.linkage(my_df, method  = "ward"), orientation="left", leaf_font_size=8, labels=my_df.index)
	plt.title(my_title)
	plt.xlabel('Items')
	plt.ylabel('Euclidean distances')
	plt.savefig(working_dir+my_title+".png", bbox_inches = "tight", pad_inches=0.3)
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


def draw_item_clusters_by_parameter_setting_avgs(my_df, param_settings, my_title):
	all_ps_avg_df = 0
	for ps in param_settings:
		ps_df = 0
		for index in my_df:  ## index here is a model name, e.g., "T_ldh_r1"
			if ps in index:
				if type(ps_df) == int:
					ps_df = my_df[index].to_frame()
				else:
					ps_df = pd.concat([ps_df, my_df[index]], axis=1)
		ps_avg_df = ps_df.mean(axis=1).to_frame()
		ps_avg_df.columns = [ps.strip("_")]
		if type(all_ps_avg_df) == int:
			all_ps_avg_df = ps_avg_df
		else:
			all_ps_avg_df = pd.concat([all_ps_avg_df, ps_avg_df], axis=1)
		draw_df_cluster(ps_avg_df, my_title+"_"+ps.strip("_"))
	draw_df_cluster(all_ps_avg_df, my_title)
					

def main():
	source_csv = working_dir+"all_spearman_N70-clustering_vectors.csv"
	raw_df = pd.read_csv(source_csv, index_col=0)
	depform_settings = ["ldh", "xdh", "xdx"]
	r1r2_settings = ["r1", "r2"]
	TU_settings = ["T_", "U_"]
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
	draw_item_clusters_by_parameter_setting_avgs(raw_df, depform_settings, "raw_model_scores_by_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, depform_settings, "ranked_model_scores_by_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(raw_df, TU_settings, "raw_model_scores_by_TU_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, TU_settings, "ranked_model_scores_by_TU_avgs")
	draw_item_clusters_by_parameter_setting_avgs(raw_df, r1r2_settings, "raw_model_scores_by_r1r2_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, r1r2_settings, "ranked_model_scores_by_r1r2_avgs")
## 2020/10/16. Working here... Above I generate clusters based on specific models (which combine all three parameters), and based on individual parameter settings; It might be good to also look at combinations of two parameters. It would be easy enough to do so for TU+depforms and for depforms+r1r2, because models are are named TU+depforms+r1r2, so I can just pass a list of the strings representing these combinations to the existing draw_item_clusters_by_parameter_setting_avgs; it will be harder to do for TU+r1r2, because these combinations don't appear in model names as a single contiguous string, so I'll need to do some parsing of model names to match TU+r1r2 combinations.
## Note that if I want to consider model rankings instead of model scores here, I'll need to use raw_df and do the ranking AFTER selecting the models (columns) I want; e.g. if I'm only interested in T_ models, I want those models ranked 1-6 because there are 6 T_ models, not 1-12 (which would include U_ models).
### I think the raw_df.rank(axis=1) part should probably be handled outside of main(). We should just pass the raw_df to whatever function and let the function handle it as desired...

	draw_item_clusters_by_parameter_setting_avgs(raw_df, ["T_ldh", "T_xdh", "T_xdx"], "raw_model_scores_by_TU_plus_depform_avgs")



if __name__ == "__main__":
    main()
