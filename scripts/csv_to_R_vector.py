#!/usr/bin/env python


import sys, csv
from scipy.stats import rankdata


def get_source_rows(tdf):
	all_raw_vecs=[]
	all_rank_vecs=[]
	tdoc=open(tdf, 'r')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		# all_raw_vecs.append(row)
		label = row.pop(0)
		rank_only = list(rankdata(row).astype(float))
		rank_row = [label]+rank_only
		all_rank_vecs.append(rank_row)
	tdoc.close()
	# print_vectors(skipheader, all_raw_vecs)
	print("\n\n\n")
	print_vectors(skipheader, all_rank_vecs)


def print_vectors(h, ev):
	print("""', '""".join(h))
	for v in ev:
		pstring = str(v[0]).replace("-", "_")+" = c("+str(v[1])+", "+str(v[2])+", "+str(v[3])+", "+str(v[4])+", "+str(v[5])+", "+str(v[6])+", "+str(v[7])+", "+str(v[8])+", "+str(v[9])+", "+str(v[10])+", "+str(v[11])+", "+str(v[12])+", "+str(v[13])+", "+str(v[14])+", "+str(v[15])+", "+str(v[16])+", "+str(v[17])+", "+str(v[18])+", "+str(v[19])+", "+str(v[20])+", "+str(v[21])+", "+str(v[22])+", "+str(v[23])+", "+str(v[24])+", "+str(v[25])+", "+str(v[26])+", "+str(v[27])+", "+str(v[28])+", "+str(v[29])+", "+str(v[30])+")"
		# pstring = "i"+str(v[0]).zfill(2)+" = c("+str(v[1])+", "+str(v[2])+", "+str(v[3])+", "+str(v[4])+", "+str(v[5])+", "+str(v[6])+", "+str(v[7])+", "+str(v[8])+", "+str(v[9])+", "+str(v[10])+", "+str(v[11])+", "+str(v[12])+")"
		print(pstring)


def main():
	# get_source_rows("/Users/leviking/Documents/dissertation/SAILS/stats/N70/all_spearman_N70-clustering_vectors_transposed.csv")
	get_source_rows("/Users/leviking/Documents/dissertation/SAILS/stats/N70/all_spearman_N70-clustering_vectors.csv")


if __name__ == "__main__":
    main()
