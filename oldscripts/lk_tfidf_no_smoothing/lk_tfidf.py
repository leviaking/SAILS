#!/usr/bin/env python

## 2015/07/15. LK. This script runs tf-idf from a library (downloaded from: https://github.com/hrs/python-tf-idf).
## usage:
## python lk_tfidf.py mytestdoc mycorpusdirectory
## So you should have "mycorpusdirectory" in the same folder as this script. mytestdoc is the document you are analyzing with tf-idf. mycorpusdirectory should be a folder containing the documents that comprise the corpus.

import sys, tfidf
from os import walk

"""
python
import tfidf

table = tfidf.tfidf()
table.addDocument("foo", ["alpha", "bravo", "delta", "echo", "foxtrot", "golf", "hotel"])
table.addDocument("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
table.addDocument("baz", ["kilo", "lima", "mike", "november"])

print table.similarities (["alpha", "bravo", "charlie", "charlie"]) # => [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]
"""

testdocname = sys.argv[1]
mycorpusdir = sys.argv[2]
#corpusdocname = sys.argv[2]


def get_doc_names(somedir):
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	return docnames

def get_word_list(somedoc):
	wds = []
	with open(mycorpusdir+'/'+somedoc) as currdoc:
	#with open(somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for w in clist:
				wds.append(w)
	return wds

def add_to_table(currdoc):
	table.addDocument(currdoc, get_word_list(currdoc))

def get_testdoc_words(somename):
	testwords = []
	with open(somename) as testdoc:
		for tline in testdoc:
			tlist = tline.strip().split()
			tlist = filter(None, tlist)
			for w in tlist:
				testwords.append(w)
	return testwords

def run_testwords(twlist):
	all_avgs = {}
	avglist = []
	for tw in twlist:
		runningtotal = float(0)
		twscores = table.similarities([tw])
		for tws in twscores:
			#if tws[1] != 0:
			#	print "NONZERO: ", tws
			#else: pass
			runningtotal += float(tws[1])
		avgscore = runningtotal / float(len(mydocs))
		if tw in all_avgs:
			all_avgs[tw] += avgscore
		else:
			all_avgs[tw] = avgscore

	for key in all_avgs:
		avglist.append([all_avgs[key], key])
	return avglist

def pretty_print(avglist):
	avglist.sort(reverse=True)
	for pair in avglist:
		print pair[1], '\t', pair[0]

##### MAIN PROGRAM

table = tfidf.tfidf()

mydocs = get_doc_names(mycorpusdir)
#mydocs = [corpusdocname]

for mydoc in mydocs:
	add_to_table(mydoc)

mytestwords = get_testdoc_words(testdocname)

myavgs = run_testwords(mytestwords)

pretty_print(myavgs)