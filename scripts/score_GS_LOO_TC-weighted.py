#!/usr/bin/env python

##2018-08-16. LK. This script produces a Spearman correlation score for each of the scored GS files for a given item. It produces a single csv file for the item showing the various GSs for that item ranked according to Spearman. These input files are the the output files of lk_tfidf_LOO_TC.py, each of which is a csv that has a response score for each response in the GS; the response score is the result of leave-one-out testing and is a "TC" score (King and Dickinson 2016; a tf-idf cosine score). Each response has three scores -- one for each dependency format we are using (ldh (label-dependent-head), xdh and xdx). The header for these files is:
##ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx	ldh tfidf cosine	xdh tfidf cosine	xdx tfidf cosine
##The output will be stored in the "TC_Spearman" folder, which should be created in advance as a sister to the input folder.

import sys, math, csv
from os import walk
from scipy.stats import spearmanr
testitem = sys.argv[1] ##01-30 + T or U, e.g. 02T or 29T
itemextensions = ['_all_cns_LOO_TC', '_all_fns_LOO_TC', '_all_ns_LOO_TC', '_almosts_LOO_TC', '_coreyes_LOO_TC', '_perfects_LOO_TC', '_firsts_LOO_TC', '_seconds_LOO_TC']
deptypes = ['ldh', 'xdh', 'xdx']
# # outheader=['GS', 'Rank', 'Spearman', 'p-score']
outheader=['GS', 'Spearman', 'p-score']

gsdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/')
sourcedir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/LOO_TC-weighted/')
outputdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/TC_Spearman-weighted/LOO_GS/')
depcols={'ldh':11, 'xdh':12, 'xdx':13} ##the columns where the response score for each deptype is stored (zero-indexed)
anncols=[2, 3, 4, 5, 6] ## list of cols where the annotation scores are stored (zero=indexed); C,A,G,I,V

def get_source_content(tdf):
	everything=[]
	tdoc=open(sourcedir+tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return everything

## Returns a score of [.2, .4, .6, .8 or 1.0] for each response, which is basically an "average annotation" score where all 5 annotation features are weighted equally
def get_ann_score(mycsvline):
	yes_total = 0.0
	for ac in anncols:
		yes_total+=float(mycsvline[ac])
		# # print yes_total
	ann_score = (yes_total * 0.2) ## 5 total annotations, and here each is worth 1/5, thus multiply by 0.2.
	print ann_score
	return ann_score 

## allrows = list of all row lists (minus header) representing entire TC-scored csv; dtype = ldh or xdh or xdx; returns two vectors (lists):  ans = annotation score for each response, second is TC score for each response (in same order) in the given deptype form
def get_input_vectors(allrows, dtype):
	ans = []
	tcs = []
	for krow in allrows:
		a = get_ann_score(krow) ## float
		## here we assign a value to the annotation score to ensure it is non-zero
		if a < 0.01:
			a = 0.01
		else:
			pass
		ans.append(a)
		t = float(krow[depcols[dtype]]) ## float
		if t < 0.00001:
			t = 0.000001
		else:
			pass
		tcs.append(t)
	return ans, tcs

def write_output(rs, nm):
	thisfile=open(outputdir+nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()

def main():
	alloutrows = [] ## for now, 3 fields: GS name, spearman, p-score
	# # gsfns=get_GS_filenames(testitem) ##GS filenames
	for itex in itemextensions:
		itfilename = testitem+itex+"-w"
		itfilerows = get_source_content(itfilename+".csv")
		for dt in deptypes:
			annotlist, tclist = get_input_vectors(itfilerows,dt)
			# # print annotlist
			# # print tclist
			## here we calculate spearman correlation score
			myspear, myp = spearmanr(annotlist, tclist)
			alloutrows.append([itfilename+"-"+dt, myspear, myp])
	alloutrows.sort(key=lambda x: x[1])
	write_output(alloutrows, testitem+"-Spearman-GS-w.csv")
	

if __name__ == "__main__":
    main()
