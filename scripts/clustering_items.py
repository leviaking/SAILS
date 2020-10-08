#!/usr/bin/env python


import sys, csv
from scipy.stats import rankdata
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch


source_csv = "/Users/leviking/Documents/dissertation/SAILS/stats/N70/all_spearman_N70-clustering_vectors.csv"

dataset = pd.read_csv(source_csv)
full_dataset = dataset.iloc[:].values
cluster_labels = ['i01_in_dance', 'i02_tr_eat', 'i03_di_deliver', 'i04_in_wake', 'i05_di_teach', 'i06_tr_carry', 'i07_in_fly', 'i08_di_serve', 'i09_tr_ride', 'i10_in_cry', 'i11_di_ask', 'i12_tr_cut', 'i13_in_swim', 'i14_di_sell', 'i15_tr_plant', 'i16_tr_catch', 'i17_di_feed', 'i18_in_cough', 'i19_tr_photo', 'i20_in_laugh', 'i21_di_throw', 'i22_tr_forecast', 'i23_di_inject', 'i24_in_sleep', 'i25_tr_chase', 'i26_di_readto', 'i27_in_sing', 'i28_di_givedirection', 'i29_tr_cuddle', 'i30_in_run']

## column 0 contains these labels:
## 'T_ldh_r1', 'T_xdh_r1', 'T_xdx_r1', 'T_ldh_r2', 'T_xdh_r2', 'T_xdx_r2', 'U_ldh_r1', 'U_xdh_r1', 'U_xdx_r1', 'U_ldh_r2', 'U_xdh_r2', 'U_xdx_r2


def get_depform_averages(fd):
	ldh_rows = []
	xdh_rows = []
	xdx_rows = []
	for model_row in fd:
		if "ldh" in model_row[0]:
			ldh_rows.append(model_row)
		elif "xdh" in model_row[0]:
			xdh_rows.append(model_row)
		elif "xdx" in model_row[0]:
			xdx_rows.append(model_row)
		else:
			pass
	ldh_avgs = []
	xdh_avgs = []
	xdx_avgs = []
	for i in range(1,31):
		i_ldh_sum = 0
		i_xdh_sum = 0
		i_xdx_sum = 0
		for ldh_r in ldh_rows:
			i_ldh_sum += ldh_r[i]
		for xdh_r in xdh_rows:
			i_xdh_sum += xdh_r[i]
		for xdx_r in xdx_rows:
			i_xdx_sum += xdx_r[1]
		i_ldh_avg = i_ldh_sum/12.0
		i_xdh_avg = i_xdh_sum/12.0
		i_xdx_avg = i_xdx_sum/12.0
		ldh_avgs.append(i_ldh_avg)
		xdh_avgs.append(i_xdh_avg)
		xdx_avgs.append(i_xdx_avg)
	return [ldh_avgs, xdh_avgs, xdx_avgs]


def get_r1r2_averages(fd):
	r1_rows = []
	r2_rows = []
	for model_row in fd:
		if "r1" in model_row[0]:
			r1_rows.append(model_row)
		elif "r2" in model_row[0]:
			r2_rows.append(model_row)
		else:
			pass
	r1_avgs = []
	r2_avgs = []
	for i in range(1,31):
		i_r1_sum = 0
		i_r2_sum = 0
		for r1_r in r1_rows:
			i_r1_sum += r1_r[i]
		for r2_r in r2_rows:
			i_r2_sum += r2_r[i]
		i_r1_avg = i_r1_sum/12.0
		i_r2_avg = i_r2_sum/12.0
		r1_avgs.append(i_r1_avg)
		r2_avgs.append(i_r2_avg)
	return [r1_avgs, r2_avgs]


def get_TU_averages(fd):
	T_rows = []
	U_rows = []
	for model_row in fd:
		if "T_" in model_row[0]:
			T_rows.append(model_row)
		elif "U_" in model_row[0]:
			U_rows.append(model_row)
		else:
			pass
	T_avgs = []
	U_avgs = []
	for i in range(1,31):
		i_T_sum = 0
		i_U_sum = 0
		for T_r in T_rows:
			i_T_sum += T_r[i]
		for U_r in U_rows:
			i_U_sum += U_r[i]
		i_T_avg = i_T_sum/12.0
		i_U_avg = i_U_sum/12.0
		T_avgs.append(i_T_avg)
		U_avgs.append(i_U_avg)
	return [T_avgs, U_avgs]

depform_avgs = get_depform_averages(full_dataset)
depform_avgs_df = pd.DataFrame(depform_avgs)
depform_avgs_df = depform_avgs_df.T		## Transpose
r1r2_avgs = get_r1r2_averages(full_dataset)
r1r2_avgs_df = pd.DataFrame(r1r2_avgs)
r1r2_avgs_df = r1r2_avgs_df.T		## Transpose
TU_avgs = get_TU_averages(full_dataset)
TU_avgs_df = pd.DataFrame(TU_avgs)
TU_avgs_df = TU_avgs_df.T		## Transpose

depform_avgs_dendrogram = sch.dendrogram(sch.linkage(depform_avgs_df, method  = "ward"), orientation="left", leaf_font_size=8, labels=cluster_labels)
plt.title('depform_avgs')
plt.xlabel('Euclidean distances')
plt.ylabel('Items')
# plt.show()
plt.savefig("/Users/leviking/Documents/dissertation/SAILS/stats/N70/cluster_depform_avgs.png", bbox_inches="tight", pad_inches=1.0)


r1r2_avgs_dendrogram = sch.dendrogram(sch.linkage(r1r2_avgs_df, method  = "ward"), leaf_font_size=6, labels=cluster_labels)
plt.title('r1r2_avgs')
plt.xlabel('Items')
plt.ylabel('Euclidean distances')
# plt.show()
plt.savefig("/Users/leviking/Documents/dissertation/SAILS/stats/N70/cluster_r1r2_avgs.png", bbox_inches="tight", pad_inches=1.0)


TU_avgs_dendrogram = sch.dendrogram(sch.linkage(TU_avgs_df, method  = "ward"), leaf_font_size=8, labels=cluster_labels)
plt.title('TU_avgs')
plt.xlabel('Items')
plt.ylabel('Euclidean distances')
# plt.show()
plt.savefig("/Users/leviking/Documents/dissertation/SAILS/stats/N70/cluster_TU_avgs.png",  pad_inches=1.0)


# def main():
# 	# get_source_rows("/Users/leviking/Documents/dissertation/SAILS/stats/N70/all_spearman_N70-clustering_vectors_transposed.csv")
# 	get_source_rows("/Users/leviking/Documents/dissertation/SAILS/stats/N70/all_spearman_N70-clustering_vectors.csv")
# 
# 
# if __name__ == "__main__":
#     main()
