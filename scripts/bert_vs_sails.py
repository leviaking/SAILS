#!/usr/bin/env python


## 2021/03/01. This script takes the NNS files containing my system scores,
## along with the NS training files; it uses BERT to compare each NNS test
## sentence against the corresponding NS sentences. It extends each scored file
## with the BERT score and rank and stores this as a new file. The resulting
## files can now be used to generate a spearman correlation score for each
## configuration. (NTS: update get_all_spearman_correlations.py to handle this.)


from os import walk
from scipy.stats import rankdata
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('stsb-roberta-large')
model.eval()


train_sample = 'N50'
test_sample = 'N04'
testdir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'+
		 train_sample+'-VS-'+test_sample+'/')
traindir=('/Users/leviking/Documents/dissertation/SAILS/training_data/'+
		  train_sample+'/')
bert_dir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'+
		  train_sample+'-VS-'+test_sample+'-BERT/')


def get_file_names(x_dir):
	file_names = []
	for (dirpath, dirnames, filenames) in walk(x_dir):
		file_names.extend(filenames)
		break
	file_names = [dn for dn in file_names if ".csv" in dn]
	file_names.sort()
	return file_names


def match_test_and_train(tefns, trfns):
	matches = []
	for tefn in tefns:
		if "-r1-" in tefn:
			primacy = "-r1-"
		elif "-r2-" in tefn:
			primacy = "-r2-"
		itmn = tefn[:5]
		for trfn in trfns:
			if itmn in trfn:
				if primacy in trfn:
					matches.append([tefn, trfn])
	return matches


def strip_final_punct(xsentence):
	punct = [".", "?", "!", ";"]
	if xsentence[-1] in punct:
		xsentence = xsentence[:-1]
	xsentence.strip()
	return xsentence


def sentlist_to_embeddings(sl):
	xsl = [strip_final_punct(xx) for xx in sl]
	mbds = [model.encode(xs, convert_to_tensor=True) for xs in xsl]
	return(mbds)


def run_match_set(xy):
## prep test embeddings
	xtest = xy[0]
	xtdf = pd.read_csv(testdir+xtest, index_col=0)
	xt_sents = xtdf["Response"]
	xtembeddings = sentlist_to_embeddings(xt_sents)
## prep NS model embeddings
	ytrain = xy[1]
	ytdf = pd.read_csv(traindir+ytrain, index_col=0)
	ytdf_sents = ytdf["Response"]
	ytembeddings = sentlist_to_embeddings(ytdf_sents)
## run test vs NS model
	ytscores = run_one_file_pairing(xtembeddings, ytembeddings)
	# ytranks = list(rankdata(ytscores).astype(float))
	ytranks = list(rankdata([-1 * i for i in ytscores]).astype(int)) ## invert rankings
	xvy = xtdf.copy()
	xvy["BERT_score"] = ytscores
	xvy["BERT_rank"] = ytranks
	ytname = xtest.replace(".csv", "-BERT.csv")
	ytname = ytname.replace("-r", "-vs_r")
	xvy.to_csv(bert_dir+ytname)


def run_one_file_pairing(test_embeds, train_embeds):
	file_scores = []
	for tse in test_embeds:
		s_pair_scores = []
		for tre in train_embeds:
			tre_score = util.pytorch_cos_sim(tse, tre)
			s_pair_scores.append(tre_score)
		tse_score = np.average(s_pair_scores)
		file_scores.append(tse_score)
	return file_scores


def main():
	test_file_names = get_file_names(testdir)
	train_file_names = get_file_names(traindir)
	match_sets = match_test_and_train(test_file_names, train_file_names)  ## names only -- no paths
	for ms in match_sets:
		print(ms)
		run_match_set(ms)


if __name__ == "__main__":
    main()

