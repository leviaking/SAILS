#!/usr/bin/env python

##June 2020; this is branched from weighting_dependencies_experiment.py;
## Currently a work in progress... this is for comparing LDH, XDH and XDX

import sys, math, csv
from os import walk
from scipy.stats import rankdata
from scipy.stats import spearmanr

# # itemnum = testdocfn.split("_")[0]



def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if "NNS_vs_all_ns_TC_w" in dn]
	docnames.sort()
	return docnames


def get_source_rows(tdf): ## tdf ~= test doc file; returns csv lines as lists
# input header:
# ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx	ldh TC weighted	xdh TC weighted	xdx TC weighted	ldh TC unweighted	xdh TC unweighted	xdx TC unweighted
# scores are row[11] thru row[16]
	everything=[]
	tdoc=open(tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything



## columns to add (8):
## ldh w rank, xdh w rank, xdx w rank, ldh uw rank, xdh uw rank, xdx uw rank, AnnoScore, AnnoRank, 

def apply_annotation_weights(somerows):
	extended_rows = []
	##annotations are on row[2] thru row[6] (CAGIV)
	## .365 + .093 + .056 + .224 + .262 == 1 (Use these)
	for sr in somerows:
		a_score = float(sr[2]) * 0.365
		a_score = a_score + (float(sr[3]) * 0.093)
		a_score = a_score + (float(sr[4]) * 0.056)
		a_score = a_score + (float(sr[5]) * 0.224)
		a_score = a_score + (float(sr[6]) * 0.262)
		sr.append(str(a_score))
		extended_rows.append(sr)
	return extended_rows


def get_all_rankings(rrows):
	## takes full csv rows, which now include the AnnoScore; relevant columns are row[17] thru row[23]
	## from [ldh TC weighted, xdh TC weighted, xdx TC weighted, ldh TC unweighted, xdh TC unweighted, xdx TC unweighted, AnnoScore]
	## generate [ldh w rank, xdh w rank, xdx w rank, ldh uw rank, xdh uw rank, xdx uw rank, AnnoRank]
	ldh_w_scores = []
	xdh_w_scores = []
	xdx_w_scores = []
	ldh_uw_scores = []
	xdh_uw_scores = []
	xdx_uw_scores = []
	anno_scores = []
	for rr in rrows:
		ldh_w_scores.append(rr[11])
		xdh_w_scores.append(rr[12])
		xdx_w_scores.append(rr[13])
		ldh_uw_scores.append(rr[14])
		xdh_uw_scores.append(rr[15])
		xdx_uw_scores.append(rr[16])
		anno_scores.append(rr[17])
	ldh_w_ranks = list(rankdata(ldh_w_scores).astype(float))
	xdh_w_ranks = list(rankdata(xdh_w_scores).astype(float))
	xdx_w_ranks = list(rankdata(xdx_w_scores).astype(float))
	ldh_uw_ranks = list(rankdata(ldh_uw_scores).astype(float))
	xdh_uw_ranks = list(rankdata(xdh_uw_scores).astype(float))
	xdx_uw_ranks = list(rankdata(xdx_uw_scores).astype(float))
	anno_ranks = list(rankdata(anno_scores).astype(float))
	spearman_row = calculate_spearman([ldh_w_ranks, xdh_w_ranks, xdx_w_ranks, ldh_uw_ranks, xdh_uw_ranks, xdx_uw_ranks, anno_ranks])
	extended_rows = []
	for rr in rrows:
		xr = rr+[ldh_w_ranks.pop(0), xdh_w_ranks.pop(0), xdx_w_ranks.pop(0), ldh_uw_ranks.pop(0), xdh_uw_ranks.pop(0), xdx_uw_ranks.pop(0), anno_ranks.pop(0)]
		extended_rows.append(xr)
	return extended_rows, spearman_row


def calculate_spearman(allranks):
	## spearman values will go in a csv with this header:
	## (Source), ldh_w_spearman, ldh_w_p, xdh_w_spearman, xdh_w_p, xdx_w_spearman, xdx_w_p, ldh_uw_spearman, ldh_uw_p, xdh_uw_spearman, xdh_uw_p, xdx_uw_spearman, xdx_uw_p
	ldh_w_ranks = allranks[0]
	xdh_w_ranks = allranks[1]
	xdx_w_ranks = allranks[2]
	ldh_uw_ranks = allranks[3]
	xdh_uw_ranks = allranks[4]
	xdx_uw_ranks = allranks[5]
	anno_ranks = allranks[6]
	ldh_w_spr, ldh_w_p = spearmanr(ldh_w_ranks, anno_ranks)
	xdh_w_spr, xdh_w_p = spearmanr(xdh_w_ranks, anno_ranks)
	xdx_w_spr, xdx_w_p = spearmanr(xdx_w_ranks, anno_ranks)
	ldh_uw_spr, ldh_uw_p = spearmanr(ldh_uw_ranks, anno_ranks)
	xdh_uw_spr, xdh_uw_p = spearmanr(xdh_uw_ranks, anno_ranks)
	xdx_uw_spr, xdx_uw_p = spearmanr(xdx_uw_ranks, anno_ranks)
	sp_row = [ldh_w_spr, ldh_w_p, xdh_w_spr, xdh_w_p, xdx_w_spr, xdx_w_p, ldh_uw_spr, ldh_uw_p, xdh_uw_spr, xdh_uw_p, xdx_uw_spr, xdx_uw_p]
	return sp_row


def process_one_item(somefile):
	## do all the above, return item rows and spearman scores
	oldheader, sourcerows = get_source_rows(somefile)
	newheader = oldheader+['ldh w rank', 'xdh w rank', 'xdx w rank', 'ldh uw rank', 'xdh uw rank', 'xdx uw rank', 'AnnoScore', 'AnnoRank']
	sourcerows = apply_annotation_weights(sourcerows)
	rows_with_ranks, spearman_row = get_all_rankings(sourcerows)
	rows_with_ranks.insert(0, newheader)
	return rows_with_ranks, spearman_row


def average_spearman_scores():
	#### I decided this should just be handled in the spreadsheet with Excel
	## this should calculate 6 scores representing average of spearman across items
	## should also calculate 2 scores averaging the above 6 scores: weighted & unweighted
	pass


def write_output(rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()



def main():
	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/responses/TC/')
	outputdir=('/Users/leviking/Documents/dissertation/SAILS/weighting_dependencies/')
	input_files = get_infile_names(sourcedir)
	spearman_rows = [["Source", "ldh_w_spear", "ldh_w_p", "xdh_w_spear", "xdh_w_p", "xdx_w_spear", "xdx_w_p", "ldh_uw_spear", "ldh_uw_p", "xdh_uw_spear", "xdh_uw_p", "xdx_uw_spear", "xdx_uw_p"]]
	for inf in input_files:
		out_label = inf.replace("_TC_w.csv", "")
		output_rows, spearman_row = process_one_item(sourcedir+inf)
		spearman_row.insert(0, out_label)
		spearman_rows.append(spearman_row)
		write_output(output_rows, outputdir+out_label+".csv")
	write_output(spearman_rows, outputdir+"Weighting_dependencies_experiment_spearman.csv")


if __name__ == "__main__":
    main()
