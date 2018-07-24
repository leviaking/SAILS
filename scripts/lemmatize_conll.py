#!/usr/bin/env python

## 2015/07/13. LK.
###USAGE:
###python lemmatize_conll.py myinput.txt
###
###This script will require (in the locations seen below):
###myinput.txt (the plain text; although, this script doesn't really require it, only the filename)
###myinput.xml (the output of the stanford corenlp lemmatizer)
###myinput.LKconll (the dependency parsed output of the stanford parser; note the "LK" -- in some cases we'll have both .conll and .LKconll; in such cases, the .conll is the original .conll file (probably not parsed by me (e.g., a download of the PTB in .conll format)), and the .LKconll file is the conll dependency parse resulting from a parse using MY parameters.
###
###This script will write out a conll format file where the words have been replaced by their lemmas.

import sys

textname=sys.argv[1]
gshome=textname.split('/')
gshome='/'.join(gshome[:-2])
textprefix=textname.split('/')[-1]
textprefix=textprefix.split('.')[0]
xmlname=gshome+'/lemmaxml/'+textprefix+'.xml'
conllname=gshome+'/LKconll/'+textprefix+'.LKconll'
lemma_conll_name = gshome+'/lemma_conll/'+textprefix+'.lemma_conll'

### This is the portion of the script that handled collecting lemma sentences from the xml files in the pilot studies (2013-2016 papers). It had problems handling any response that looked like a fragment, contained two or more sentences (on one line) or had sentence internal periods. It wasn't a big problem for the pilot studies, but it is a problem for the much larger datasets in the 2018 SAILS work. This older method may be more appropriate for cleaner data, because the changed version that follows is written to handle multiple xml files concatenated into one file (this is because the lemmatizer cannot be forced to handle each line as a separate sentence; instead it decides some lines are fragments and concatenates the fragment with the subsequent line; to prevent this, I have to load the lemmatizer model anew for each line.)
# # xmlsents=[]
# # xcounter = 1
# # with open(xmlname, 'rU') as xmlfile:
# # 	current_xsent = []
# # 	current_wdlem = []
# # 	for xline in xmlfile:
# # 		xline=xline.strip()
# # 		###2018/07/11: ATTENTION! I'm pretty dang sure the problem is somewhere in the remainder of this loop! I think I'm splitting on things or matching things here, and there must be some exceptions to the cases I've laid out.
# # 		if xline.startswith('<word>'):
# # 			wd = xline.split('<word>')[1].split('</word>')[0]
# # 			current_wdlem.append(wd)
# # 		elif xline.startswith('<lemma>'):
# # 			lem = xline.split('<lemma>')[1].split('</lemma>')[0]
# # 			current_wdlem.append(lem)
# # 			current_xsent.append(current_wdlem)
# # 			current_wdlem=[]
# # 		elif xline.startswith('</sentence>'):
# # 			xmlsents.append(current_xsent)
# # 			current_xsent = []
# # 		else:
# # 			pass
# # 		xcounter+=1
# # xmlsents = filter(None, xmlsents)
	

xmlsents=[]
xcounter = 1
with open(xmlname, 'rU') as xmlfile:
	current_xsent = []
	current_wdlem = []
	for xline in xmlfile:
		xline=xline.strip()
		###2018/07/11: ATTENTION! I'm pretty dang sure the problem is somewhere in the remainder of this loop! I think I'm splitting on things or matching things here, and there must be some exceptions to the cases I've laid out.
		if xline.startswith('<word>'):
			wd = xline.split('<word>')[1].split('</word>')[0]
			try:
				wd=str(wd).lower()
			except: pass
			current_wdlem.append(wd)
		elif xline.startswith('<lemma>'):
			lem = xline.split('<lemma>')[1].split('</lemma>')[0]
			try:
				lem=str(lem).lower()
			except: pass
			current_wdlem.append(lem)
			current_xsent.append(current_wdlem)
			current_wdlem=[]
		#elif xline.startswith('</sentence>'): ##actually, I think this is the only change needed here.
		elif xline.startswith('</root>'):
			xmlsents.append(current_xsent)
			current_xsent = []
		else:
			pass
		xcounter+=1
xmlsents = filter(None, xmlsents)

conllsents = []
ccounter = 1
with open(conllname, 'rU') as conllfile:
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
	#print len(csent)
	try:
		lsent=xmlsents.pop(0)
	except:
		lsent=[]
	#lsent = xmlsents.pop(0) ##getting the error below on some files, which fail to write output file
# 	Traceback (most recent call last):
#   File "/Users/leviking/Documents/dissertation/SAILS/scripts/lemmatize_conll.py", line 69, in <module>
#     lsent = xmlsents.pop(0)
# IndexError: pop from empty list
	#print len(lsent)
	#print '\n'
	if len(csent) != len(lsent): ###this part is problematic in some cases involving non-standard punctuation, e.g. ";)" and similar "punctuation emoticons". The parser and the lemmatizer tokenize these differently, so the length of the sentence as output from lemmatizer and parser may not match in these cases. The number of these cases is so small that it's easier to simply modify the input rather than try to account for every possible weird input...
		continue
	lc_sent=[]
	while csent:
		cwline = csent.pop(0)
		#print cwline
		lwpair = lsent.pop(0)
		#print lwpair
		#print '\n'
		lemma = lwpair[1]
		cwlist = cwline.split('\t')
		lc_line = '\t'.join([cwlist[0], lemma, cwlist[2], cwlist[3], cwlist[4], cwlist[5], cwlist[6], cwlist[7], cwlist[8], cwlist[9]])
		lc_sent.append(lc_line)
	#print '\n'
	lemcon_sents.append(lc_sent)

outfile = open(lemma_conll_name, 'w')
for lm in lemcon_sents:
	for km in lm:
		outfile.write(km)
		outfile.write('\n')
	outfile.write('\n')
outfile.close()