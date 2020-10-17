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
	plt.xlabel('Euclidean distances')
	plt.ylabel('Items')
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
	draw_df_cluster(raw_df, "raw_model_scores")  ## clusters items using all raw scores for all items and models
	draw_df_cluster(ranked_models_by_item_df, "ranked_model_scores")  ## clusters items; for each item, each model is ranked 1-12; uses all items and models
	draw_df_cluster(ranked_items_by_model_df, "ranked_item_scores")  ## clusters items; for each model, each item is ranked 1-30; uses all items and models
	draw_single_vector_clusters_from_df(raw_df, "raw_model_scores")  ## clusters items using raw scores from single model; generates 12 clusterings, 1 per model
	draw_single_vector_clusters_from_df(ranked_models_by_item_df, "ranked_model_scores")  ## clusters items; first ranks each model 1-12 for each item, then uses a single model's ranks to cluster 30 items; generates 12 clusterings, 1 per model
	draw_item_avg_clusters(raw_df, "item_avg_raw_scores")  ## clusters items; for each item, it uses the item's average score from all 12 models
	draw_item_avg_clusters(ranked_items_by_model_df, "item_avg_ranked_scores")  ## clusters items; first ranks each item 1-30 for each model, then takes the average rank for each item
	draw_item_median_clusters(raw_df, "item_median_raw_scores")  ## clusters items; for each item, it uses the item's median score from all 12 models
	draw_item_median_clusters(ranked_items_by_model_df, "item_median_ranked_scores")  ## clusters items; first ranks each item 1-30 for each model, then takes the median rank for each item
	draw_item_clusters_by_parameter_setting_avgs(raw_df, depform_settings, "raw_model_scores_by_depform_avgs")  ## clusters items; for each item, the average score is calculated for all ldh models, all xdh models, all xdx models; clusters based on these three values
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, depform_settings, "ranked_model_scores_by_depform_avgs")  ## clusters items; for each item, the average rank is calculated for all ldh models, all xdh models, all xdx models; clusters based on these three values
	draw_item_clusters_by_parameter_setting_avgs(raw_df, TU_settings, "raw_model_scores_by_TU_avgs")  ## clusters items; for each item, the average score is calculated for all Targeted models, all Untargeted models; clusters based on these two values
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, TU_settings, "ranked_model_scores_by_TU_avgs")  ## clusters items; for each item, the average rank is calculated for all Targeted models, all Untargeted models; clusters based on these two values
	draw_item_clusters_by_parameter_setting_avgs(raw_df, r1r2_settings, "raw_model_scores_by_r1r2_avgs")  ## clusters items; for each item, the average score is calculated for all r1 models, all r2 models; clusters based on these two values
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, r1r2_settings, "ranked_model_scores_by_r1r2_avgs")  ## clusters items; for each item, the average rank is calculated for all r1 models, all r2 models; clusters based on these two values

## 2020/10/16. Working here... Above I generate clusters based on specific models (which combine all three parameters), and based on individual parameter settings; It might be good to also look at combinations of two parameters. It would be easy enough to do so for TU+depforms and for depforms+r1r2, because models are are named TU+depforms+r1r2, so I can just pass a list of the strings representing these combinations to the existing draw_item_clusters_by_parameter_setting_avgs; it will be harder to do for TU+r1r2, because these combinations don't appear in model names as a single contiguous string, so I'll need to do some parsing of model names to match TU+r1r2 combinations.
## Note that if I want to consider model rankings instead of model scores here, I'll need to use raw_df and do the ranking AFTER selecting the models (columns) I want; e.g. if I'm only interested in T_ models, I want those models ranked 1-6 because there are 6 T_ models, not 1-12 (which would include U_ models).
### I think the raw_df.rank(axis=1) part should probably be handled outside of main(). We should just pass the raw_df to whatever function and let the function handle it as desired...

	draw_item_clusters_by_parameter_setting_avgs(raw_df, ["U_ldh", "U_xdh", "U_xdx"], "raw_model_scores_by_TU_plus_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(raw_df, ["T_ldh", "T_xdh", "T_xdx"], "raw_model_scores_by_TU_plus_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(raw_df, ["ldh_r1", "xdh_r1", "xdx_r1"], "raw_model_scores_by_depform_plus_r1r2_avgs")
	draw_item_clusters_by_parameter_setting_avgs(raw_df, ["ldh_r2", "xdh_r2", "xdx_r2"], "raw_model_scores_by_depform_plus_r1r2_avgs")

## 2020/10/17. These are of questionable validity... Because this filters out some of the models, we should assign them rankings AFTER this filtering... This approach does the rankings BEFORE
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, ["U_ldh", "U_xdh", "U_xdx"], "ranked_model_scores_by_TU_plus_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, ["T_ldh", "T_xdh", "T_xdx"], "ranked_model_scores_by_TU_plus_depform_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, ["ldh_r1", "xdh_r1", "xdx_r1"], "ranked_model_scores_by_depform_plus_r1r2_avgs")
	draw_item_clusters_by_parameter_setting_avgs(ranked_models_by_item_df, ["ldh_r2", "xdh_r2", "xdx_r2"], "ranked_model_scores_by_depform_plus_r1r2_avgs")



if __name__ == "__main__":
    main()
