#!/usr/bin/env python

#2015/09/02. LK. We're not currently using this tool. The WSJ and Brown corpora both come as collections of small files (I think WSJ has 1,639), so we're just keeping the data in divided up according to the original files rather than splitting it up into files of some custom size for tfidf. We think it will work just fine using the original division.

## 2015/07/15. LK. This script takes a text document (ONE SENTENCE PER LINE) and splits it up into smaller documents. This was written for the purpose of taking a single large corpus and splitting it up into smaller documents, because tfidf uses a count of the number of documents a term occurs in. We're currently trying to run tf-idf on documents (SAILS gold standards) of 14 sentences each * 7 words per sentence (avg) = 98 words. So I'm setting the interval (see variable "interval" below) to 98 (not anymore), and this script will output sub-documents with 98 words or more (it cuts at the nearest sentence break after the interval).

import sys, os

fulldocname = sys.argv[1]
fname = fulldocname.split('.')
dirname = fname[0]+'_'+fname[-1]
interval = 500

os.mkdir(dirname)

docnum = 0
#currdocname = fname[0]+(str(docnum).zfill(4))
currdoc = open(dirname+'/'+fname[0]+(str(docnum).zfill(4))+'.'+fname[-1], 'w+')

with open(fulldocname) as fulldoc:
	wdcount = 0
	currdoclines = []
	for fline in fulldoc:
		currdoclines.append(fline)
		wdcount += len(fline.split(' '))
		if wdcount >= interval:
			for cdl in currdoclines:
				currdoc.write(cdl)
				currdoc.write('\n')
			currdoc.close()
			docnum += 1
			currdoclines = []
			wdcount = 0
			currdoc = open(dirname+'/'+fname[0]+(str(docnum).zfill(4))+'.'+fname[-1], 'w+')
		else: pass
	for cdl in currdoclines:
		currdoc.write(cdl)
		currdoc.write('\n')
	currdoc.close()
