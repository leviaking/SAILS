#!/usr/bin/env python

## 2019/06/22. LK. This script is run after text_to_lemmatized_conll.py / .sh, at which point the NNS responses have all been parsed and lemmatized. The lemmatized dependency parses are stored in /Users/leviking/Documents/dissertation/SAILS/responses/lemma_conll. The corresponding csvs are stored in /Users/leviking/Documents/dissertation/SAILS/responses/rawcsvs. This script should simply add each lemma_conll parse to the corresponding line of the corresponding rawcsv file.

import sys, re, csv, datetime, os
from shutil import copyfile

csvdir=('/Users/leviking/Documents/dissertation/SAILS/responses/rawcsvs/')
lcdir=('/Users/leviking/Documents/dissertation/SAILS/responses/lemma_conll/')
lkconlldir=('/Users/leviking/Documents/dissertation/SAILS/responses/LKconll/')
penndir=('/Users/leviking/Documents/dissertation/SAILS/responses/penn/')
txtdir=('/Users/leviking/Documents/dissertation/SAILS/responses/txt/')
lemmaxmldir=('/Users/leviking/Documents/dissertation/SAILS/responses/lemmaxml/')
finaldir=('/Users/leviking/Documents/dissertation/SAILS/responses/finalcsvs/')


def get_all_lemma_conll_filenames(): ##this will get a list of all the files in the lemma_conll directory; these are the files that were fully processed... when we run this, the only files in the lemma_conll folder should be the desired *.lemma_conll files, and these are the files that provide the parses that we apply to the other files.
	for stuff in os.walk('/Users/leviking/Documents/dissertation/SAILS/responses/lemma_conll/'):
		mystuff=stuff[2]
	return mystuff

def get_handles(lcnames):
	hs=[]
	for lcn in lcnames:
		handle=lcn.split('.')[0]
		hs.append(handle)
	hs.sort()
	return hs


def copy_rawcsvs(handles): ##this copies the csvs from responses/rawcsvs/ to responses/final_csvs/.
	for handle in handles:
		copyfile(csvdir+handle+'.csv', finaldir+handle+'_lc.csv')

def get_parse_dict(h):
	hdict={}
	respids=[]
	idsource=open(csvdir+h+'.csv', 'rU')
	sreader=csv.reader(idsource, dialect=csv.excel)
	skipheader=next(sreader, None)
	for srow in sreader:
		respid=srow[0]
		respids.append(respid)
	idsource.close()
	parsesource=open(lcdir+h+'.lemma_conll', 'rU')
	parsefull=parsesource.read()
	parses=parsefull.split('\n\n')
	filter(None, parses)
	while respids:
		r=respids.pop(0)
		p=parses.pop(0)
		hdict[r]=p
	return hdict

def fill_csvs_with_parse(handle, pdict):
	item=handle.split('.')[0] ##e.g. 'I01T'
	##We also need to create:
	extension='.csv'
	# # for other in others:
	sourcerows=[]
	sourcepath=csvdir+item+extension
	source=open(sourcepath, 'rU')
	sourcereader=csv.reader(source, dialect=csv.excel)
	fname=finaldir+item+extension
	fin=open(fname, 'w')
	finwriter=csv.writer(fin, dialect=csv.excel)
	header=next(sourcereader, None)
	header=header+['parse']
	finwriter.writerow(header)
	for sourcerow in sourcereader:
		sourcerows.append(sourcerow)
	source.close()
	for sr in sourcerows:
		sr=filter(None, sr)
		if sr:
			rid=sr[0]
			parse=pdict[rid]
			#print parse
			#print rid
			finrow=sr+[parse]
			#print finrow
			finwriter.writerow(finrow)
		else:
			pass
	fin.close()


myfiles=get_all_lemma_conll_filenames()
hs=get_handles(myfiles)
for hx in hs:
	pd=get_parse_dict(hx)
	fill_csvs_with_parse(hx, pd)
