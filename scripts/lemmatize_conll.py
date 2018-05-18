#!/usr/bin/env python

## 2015/07/13. LK.
###USAGE:
###python lemmatize_conll.py myinput.txt
###
###This script will require in the SAME folder:
###myinput.txt (the plain text; although, this script doesn't really require it, only the filename)
###myinput.xml (the output of the stanford corenlp lemmatizer)
###myinput.LKconll (the dependency parsed output of the stanford parser; note the "LK" -- in some cases we'll have both .conll and .LKconll; in such cases, the .conll is the original .conll file (probably not parsed by me (e.g., a download of the PTB in .conll format)), and the .LKconll file is the conll dependency parse resulting from a parse using MY parameters.
###
###This script will write out a conll format file where the words have been replaced by their lemmas.

import sys

textname=sys.argv[1]
textprefix = textname.split('.')[0]
xmlname=textprefix+'.xml'
conllname=textprefix+'.LKconll'
lemma_conll_name = textprefix+'.lemma_conll'

xmlsents=[]
xcounter = 1
with open(xmlname) as xmlfile:
	current_xsent = []
	current_wdlem = []
	for xline in xmlfile:
		xline=xline.strip()
		if xline.startswith('<word>'):
			wd = xline.split('<word>')[1].split('</word>')[0]
			current_wdlem.append(wd)
		elif xline.startswith('<lemma>'):
			lem = xline.split('<lemma>')[1].split('</lemma>')[0]
			current_wdlem.append(lem)
			current_xsent.append(current_wdlem)
			current_wdlem=[]
		elif xline.startswith('</sentence>'):
			xmlsents.append(current_xsent)
			current_xsent = []
		else:
			pass
		xcounter+=1
xmlsents = filter(None, xmlsents)
	
conllsents = []
ccounter = 1
with open(conllname) as conllfile:
	current_csent = []
	for cline in conllfile:
		cline = cline.strip()
		if cline == '':
			pass
		else:		
			if cline.startswith('1\t') and current_csent: ## "and current_csent" bc we don't want to append the empty list when we initialize on the first line
				conllsents.append(current_csent)
				current_csent=[cline]
			else:
				current_csent.append(cline)
	conllsents.append(current_csent)

lemcon_sents = [] #lemmatized conll sentences; the same as "conllsents" but with the words replaced with lemmas

while conllsents:
	csent = conllsents.pop(0)
	print len(csent)
	lsent = xmlsents.pop(0)
	print len(lsent)
	print '\n'
	if len(csent) != len(lsent):
		continue
	lc_sent=[]
	while csent:
		cwline = csent.pop(0)
		print cwline
		lwpair = lsent.pop(0)
		#print lwpair
		#print '\n'
		lemma = lwpair[1]
		cwlist = cwline.split('\t')
		lc_line = '\t'.join([cwlist[0], lemma, cwlist[2], cwlist[3], cwlist[4], cwlist[5], cwlist[6], cwlist[7], cwlist[8], cwlist[9]])
		lc_sent.append(lc_line)
	print '\n'
	lemcon_sents.append(lc_sent)

outfile = open(lemma_conll_name, 'w')
for lm in lemcon_sents:
	for km in lm:
		outfile.write(km)
		outfile.write('\n')
	outfile.write('\n')
outfile.close()