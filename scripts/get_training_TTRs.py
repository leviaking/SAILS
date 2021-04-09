#!/usr/bin/env python


## 2020/07/25. This script finds all the test files in the test directory, then finds all the corresponding training files, then trains a model from each training file and uses these models to score all the test files; a scored version of each test file is written to a new file in the output directory. A separate file is written per model, per test_response, per dependency_format; this file contains the union vector of all terms in the model and test, along with the model tf-idf vector and test tf-idf vector (for those same terms). The vast majority won't be needed but these could help me explain trends later if I need to examine the processing closely.

import sys, math, csv
from os import walk
from scipy.spatial.distance import cosine


def get_terms_list(somedoc, d):
	terms = []
	with open(refcorpusdir+d+'/'+somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for t in clist:
				terms.append(t)
	return terms


def get_training_file_names(tr_dir): 
	training_file_names = []
	for (dirpath, dirnames, filenames) in walk(tr_dir):
		training_file_names.extend(filenames)
		break
	training_file_names.sort()
	return training_file_names


def get_source_content(tdf):
	everything=[]
	tdoc=open(tdf, 'r')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def string_list_to_real_list(uglyrow, dtype):
	pylist = uglyrow[depcols[dtype]]
	pylist = pylist[1:-1]
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%")
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist


def get_test_tokens(trow, dt):
	tts = string_list_to_real_list(trow, dt)
	return tts


def get_tokens(gsrows, dty):
	gsts=[]
	for gsrow in gsrows:
		rtokens = string_list_to_real_list(gsrow,dty)
		gsts.append(rtokens)
	return gsts



samplename = "N14"
sample_n = 14.0
testdir=('/Users/leviking/Documents/dissertation/SAILS/test_data/N70/')
trainingdir=('/Users/leviking/Documents/dissertation/SAILS/training_data/'
			 +samplename+"/")
scored_vecs_dir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'
				 +samplename+'-VS-N70/')
refcorpusdir=('/Users/leviking/Documents/dissertation/SAILS_annex/brown/')
depcols={'ldh':8, 'xdh':9, 'xdx':10}


def main():
	tr_filenames = get_training_file_names(trainingdir)
	all_rows = []
	in_sum = 0
	tr_sum = 0
	di_sum = 0
	for trainingfn in tr_filenames:
		header, curr_tr_rows=get_source_content(trainingdir+trainingfn)
		# print("##########################")
		for ctr in curr_tr_rows:
			txt = ctr[1]
			txt = txt.replace(".", " ")
			txt = txt.replace("?", " ")
			txt = txt.replace("!", " ")
			txt = txt.replace("  ", " ")
			txt = txt.strip()
			txt = txt.split(" ")
			txt = [t for t in txt if t]
			if "-In-" in trainingfn:
				in_sum += len(txt)
			elif "-Tr-" in trainingfn:
				tr_sum += len(txt)
			elif "-Di-" in trainingfn:
				di_sum += len(txt)
			else:
				pass
	denom = 40.0*sample_n
	in_ttr = float(in_sum) / denom
	tr_ttr = float(tr_sum) / denom
	di_ttr = float(di_sum) / denom
	print("intransitives avg length: "+str(in_ttr))
	print("transitives avg length: "+str(tr_ttr))
	print("ditransitives avg length: "+str(di_ttr))
		# print("##########################")
		


if __name__ == "__main__":
    main()

