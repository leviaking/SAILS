#!/usr/bin/env python


## 2021/02/23. Adapted from get_stats_from_spearman.py
## Takes the csv of 360 Spearman scores and generates the desired averages (and
## other stats) according to parameters.


import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr
import pandas


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	# # docnames = [dn for dn in docnames if "NNS_vs_all_ns_TC_w" in dn]
	docnames = [dn for dn in docnames if "NNS_vs_all_ns_TC_w" in dn]
	docnames.sort()
	return docnames


def get_source_rows(tdf):
	## header row:
	"""Source	ldh_spear	ldh_p	xdh_spear	xdh_p	xdx_spear	xdx_p"""
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
	sd = {}
	for rw in rws:
		sd[rw[0]] = [float(rw[1]), float(rw[3]), float(rw[5])]
		# sd[rw[0]] = [rw[1], rw[2], rw[3], rw[4], rw[5], rw[6]]
	return sd	


def get_descriptive_stats(sd):
	# Compare dependency formats for all models
	ldh_all = []
	xdh_all = []
	xdx_all = []
	# Compare first responses (r1) vs first+second mixed (r2) for all models 
	r1_all = []
	r2_all = []
	# Compare intransitives vs transitives vs ditransitives
	in_ldh = []
	tr_ldh = []
	di_ldh = []
	# Compare all targeted models vs all untargeted models
	targ_ldh = []
	untarg_ldh = []
	# Compare targeted/untargeted x r1/r2
	targ_r1_ldh = []
	targ_r2_ldh = []
	untarg_r1_ldh = []
	untarg_r2_ldh = []
	# Compare r1/r2 x intrans/trans/ditrans for ldh models
	r1_in_ldh = []
	r2_in_ldh = []
	r1_tr_ldh = []
	r2_tr_ldh = []
	r1_di_ldh = []
	r2_di_ldh = []
	#
	for mn in sd:
		ldh_all.append(sd[mn][0])
		xdh_all.append(sd[mn][1])
		xdx_all.append(sd[mn][2])
	ldh_df = pandas.DataFrame(ldh_all)
	xdh_df = pandas.DataFrame(xdh_all)
	xdx_df = pandas.DataFrame(xdx_all)
	print("\n###### Dependency formats ######")
	print("\n\nLDH stats:")
	print(ldh_df)
	ldh_descriptive = ldh_df.describe()
	print(ldh_descriptive)
	print("\n\nXDH stats:")
	xdh_descriptive = xdh_df.describe()
	print(xdh_descriptive)
	print("\n\nXDX stats:")
	xdx_descriptive = xdx_df.describe()
	print(xdx_descriptive)
	print ("\n\n#########################################\n\n")
	print("###### First responses vs first & second mixed ######")
	for mn in sd:
		if "r1" in mn:
			r1_all.append(sd[mn][0])
			r1_all.append(sd[mn][1])
			r1_all.append(sd[mn][2])
		elif "r2" in mn:
			r2_all.append(sd[mn][0])
			r2_all.append(sd[mn][1])
			r2_all.append(sd[mn][2])
		else: pass
	r1_all_df = pandas.DataFrame(r1_all)
	r2_all_df = pandas.DataFrame(r2_all)
	print("\n\nFirst responses (all) stats:")
	r1_all_descriptive = r1_all_df.describe()
	print(r1_all_descriptive)
	print("\n\nFirst & Second responses (all) stats:")
	r2_all_descriptive = r2_all_df.describe()
	print(r2_all_descriptive)
	print ("\n\n#########################################\n\n")
	print("###### Intransitive vs Transitive vs Ditransitive ######")
	for mn in sd:
		if "In" in mn:
			in_ldh.append(sd[mn][0])
		elif "Tr" in mn:
			tr_ldh.append(sd[mn][0])
		elif "Di" in mn:
			di_ldh.append(sd[mn][0])
		else: pass
	in_ldh_df = pandas.DataFrame(in_ldh)
	tr_ldh_df = pandas.DataFrame(tr_ldh)
	di_ldh_df = pandas.DataFrame(di_ldh)
	print("\n\nIntransitives (ldh) stats:")
	in_ldh_descriptive = in_ldh_df.describe()
	print(in_ldh_descriptive)
	print("\n\nTransitives (ldh) stats:")
	tr_ldh_descriptive = tr_ldh_df.describe()
	print(tr_ldh_descriptive)
	print("\n\nDitransitives (ldh) stats:")
	di_ldh_descriptive = di_ldh_df.describe()
	print(di_ldh_descriptive)
	#
	print ("\n\n#########################################\n\n")
	print("###### Targeted vs Untargeted (ldh) ######")
	for mn in sd:
		if "T-" in mn:
			targ_ldh.append(sd[mn][0])
			if "r1" in mn:
				targ_r1_ldh.append(sd[mn][0])
			elif "r2" in mn:
				targ_r2_ldh.append(sd[mn][0])
			else: pass
		elif "U-" in mn:
			untarg_ldh.append(sd[mn][0])
			if "r1" in mn:
				untarg_r1_ldh.append(sd[mn][0])
			elif "r2" in mn:
				untarg_r2_ldh.append(sd[mn][0])
			else: pass
	targ_ldh_df = pandas.DataFrame(targ_ldh)
	untarg_ldh_df = pandas.DataFrame(untarg_ldh)
	print("\n\nTargeted Item (ldh) stats:")
	targ_ldh_descriptive = targ_ldh_df.describe()
	print(targ_ldh_descriptive)
	print("\n\nUntargeted Item (ldh) stats:")
	untarg_ldh_descriptive = untarg_ldh_df.describe()
	print(untarg_ldh_descriptive)
	#
	print ("\n\n#########################################\n\n")
	print("###### Targeted/Untargeted x First Response/First+Second (ldh) ######")
	targ_r1_ldh_df = pandas.DataFrame(targ_r1_ldh)
	targ_r2_ldh_df = pandas.DataFrame(targ_r2_ldh)
	untarg_r1_ldh_df = pandas.DataFrame(untarg_r1_ldh)
	untarg_r2_ldh_df = pandas.DataFrame(untarg_r2_ldh)
	print("\n\nTargeted R1 (ldh) stats:")
	targ_r1_ldh_descriptive = targ_r1_ldh_df.describe()
	print(targ_r1_ldh_descriptive)
	print("\n\nTargeted R2 (ldh) stats:")
	targ_r2_ldh_descriptive = targ_r2_ldh_df.describe()
	print(targ_r2_ldh_descriptive)
	print("\n\nUntargeted R1 (ldh) stats:")
	untarg_r1_ldh_descriptive = untarg_r1_ldh_df.describe()
	print(untarg_r1_ldh_descriptive)
	print("\n\nUntargeted R2 (ldh) stats:")
	untarg_r2_ldh_descriptive = untarg_r2_ldh_df.describe()
	print(untarg_r2_ldh_descriptive)
	print ("\n\n#########################################\n\n")
	print("###### intrans/trans/ditransitive x First/First+Second response (ldh) ######")
	for mn in sd:
		if "r1" in mn:
			if "In" in mn:
				r1_in_ldh.append(sd[mn][0])
			elif "Tr" in mn:
				r1_tr_ldh.append(sd[mn][0])
			elif "Di" in mn:
				r1_di_ldh.append(sd[mn][0])
			else: pass
		elif "r2" in mn:
			if "In" in mn:
				r2_in_ldh.append(sd[mn][0])
			elif "Tr" in mn:
				r2_tr_ldh.append(sd[mn][0])
			elif "Di" in mn:
				r2_di_ldh.append(sd[mn][0])
			else: pass			
	r1_in_ldh_df = pandas.DataFrame(r1_in_ldh)
	r2_in_ldh_df = pandas.DataFrame(r2_in_ldh)
	r1_tr_ldh_df = pandas.DataFrame(r1_tr_ldh)
	r2_tr_ldh_df = pandas.DataFrame(r2_tr_ldh)
	r1_di_ldh_df = pandas.DataFrame(r1_di_ldh)
	r2_di_ldh_df = pandas.DataFrame(r2_di_ldh)
	print("\n\nR1 Intrans (ldh) stats:")
	r1_in_ldh_descriptive = r1_in_ldh_df.describe()
	print(r1_in_ldh_descriptive)
	print("\n\nR2 Intrans (ldh) stats:")
	r2_in_ldh_descriptive = r2_in_ldh_df.describe()
	print(r2_in_ldh_descriptive)
	print("\n\nR1 Trans (ldh) stats:")
	r1_tr_ldh_descriptive = r1_tr_ldh_df.describe()
	print(r1_tr_ldh_descriptive)
	print("\n\nR2 Trans (ldh) stats:")
	r2_tr_ldh_descriptive = r2_tr_ldh_df.describe()
	print(r2_tr_ldh_descriptive)
	print("\n\nR1 Ditrans (ldh) stats:")
	r1_di_ldh_descriptive = r1_di_ldh_df.describe()
	print(r1_di_ldh_descriptive)
	print("\n\nR2 Ditrans (ldh) stats:")
	r2_di_ldh_descriptive = r2_di_ldh_df.describe()
	print(r2_di_ldh_descriptive)

"""	
desired comparisons:
item (inum+targ)
targ
first
verb
depform

finding optimal targeting (ldh only for now):
targ vs verb
targ vs first

finding optimal setting: first responses vs first and second mixed (ldh only for now)
first vs verb


finding optimal depform:
targ vs depform
verb vs depform
first vs depform
"""


def main():
	working_dir=("/Users/leviking/Documents/dissertation/SAILS/stats/N70/")
	all_spearman_file = "all_spearman_N70.csv"
	# spearman_rows = [["Source", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]]
	oldheader, all_spearman_rows = get_source_rows(working_dir+all_spearman_file)
	spearman_dict = get_spearman_dict(all_spearman_rows)
	get_descriptive_stats(spearman_dict)


if __name__ == "__main__":
    main()
