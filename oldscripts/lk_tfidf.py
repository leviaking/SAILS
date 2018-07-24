#!/usr/bin/env python

## 2016/04/04. LK. This script runs a *true* variant of tf-idf. It is adapted from an older script which runs an *untrue* similar algorithm, which we called "importance score" in our initial BEA2016 submission. The older script is now named lk_importance.py (and lk_importance.sh).
## Per a 2016/04/04 discussion with MD, our implementation of tf-idf for a given term in the test doc ("GS", or the like) is like this:
#raw frequency of term in GS * log(Number of docs in corpus/(1 + number of docs where term appears))
## usage: (See the shell script lk_tfidf.sh)
## python lk_tfidf.py mytestdoc mycorpusdirectory
## So you should have "mycorpusdirectory" in the same folder as this script. mytestdoc is the document you are analyzing with tf-idf. mycorpusdirectory should be a folder containing the documents that comprise the corpus.

import sys, math
from os import walk

testdocpathandname = sys.argv[1] 
mycorpusdir = sys.argv[2]


def get_doc_names(somedir):
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	return docnames

def get_word_list(somedoc):
	wds = []
	with open(mycorpusdir+'/'+somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for w in clist:
				wds.append(w)
	return wds

def add_to_table(currdoc, tbl):
	tbl.addDocument(currdoc, get_word_list(currdoc))
	return tbl

def get_testdoc_tokens(somename):
	testtokens = []
	with open(somename) as testdoc:
		for tline in testdoc:
			tlist = tline.strip().split()
			tlist = filter(None, tlist)
			for token in tlist:
				testtokens.append(token)
	return testtokens

def get_term_tfidf_list(doclist, tokenlist): ##returns a list, a la: [(<tfidf_score>, <term>), (0.00229568411387, 'nsubj$@%boy$@%play')]
	total_number_corpus_docs = len(doclist)
	tfidf_scores_and_terms_pairlist = []
	typelist=[]
	for token in tokenlist:
		if token not in typelist:
			typelist.append(token)
		else: pass
	for wordtype in typelist:
		testdoc_term_raw_freq = tokenlist.count(wordtype)
		num_of_docs_with_term = 0
		for refdoc in doclist:
			reftokens = get_word_list(refdoc)
			if wordtype in reftokens:
				num_of_docs_with_term += 1
			else: pass
		wordtype_tfidf = testdoc_term_raw_freq * (math.log(total_number_corpus_docs/(1.0 + num_of_docs_with_term)))
		#wordtype_tfidf = testdoc_term_raw_freq * (total_number_corpus_docs/(1 + num_of_docs_with_term))
		tfidf_scores_and_terms_pairlist.append((wordtype_tfidf, wordtype))
	return tfidf_scores_and_terms_pairlist
		
def pretty_print(avglist):
	avglist.sort(reverse=True)
	for pair in avglist:
		print pair[1], '\t', pair[0]

def main():
	#table = tfidf.tfidf()
	mydocs = get_doc_names(mycorpusdir) ##mydocs is the names without the paths
	# for mydoc in mydocs:
	# 	table = add_to_table(mydoc, table)
	mytesttokens = get_testdoc_tokens(testdocpathandname)
	term_tfidf_list = get_term_tfidf_list(mydocs, mytesttokens)
	# myavgs = run_testwords(mytestwords, table, mydocs)
	pretty_print(term_tfidf_list)

if __name__ == "__main__":
    main()
