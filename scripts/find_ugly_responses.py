#!/usr/bin/env python

## 2018/07/13. LK. This script is intended to find responses that contain sentence-final punctuation ('.', '!', '?') that occurs somewhere other than at the end of the response. Examples:
##T.he waiter is showing the woman a roasted turkey.
##This boy is carrying a large sack filled with groceries.See all the fruit in this sack?
##
##Responses like these cause a problem for my pipeline that takes the responses from plain text to a lemmatized conll file. (Specifically, the problem involves the Stanford lemmatizer, I believe.)
##This script operates on a directory of text files; these text files are simply the responses extracted from the master annotation files. The text files contain one response per line.
##
####USAGE: python find_ugly_responses.py path/from/scriptdirectory/to/textdirectory
####The directory argument is currently hardcoded, so the current command is simply:
####python find_ugly_responses.py

import sys, re, csv, datetime, os
from shutil import copyfile

##txtdir=sys.argv[1]
txtdir='/Users/leviking/Documents/dissertation/SAILS/sails/corpus/txt/'

for stuff in os.walk(txtdir):
	tempstuff=stuff[2]

txtflist=[]
for ts in tempstuff:
	if ts[-4:]=='.txt':
		txtflist.append(ts)
	else:
		pass
txtflist.sort()

puncts=['.', '?', '!']
##puncts=[' entr'] ##I was looking for the responses that use a diacritic in "entre"

for txfn in txtflist:
	currentuglies=[]
	#print '\n\n'+txfn
	txf = open(txtdir+txfn, 'rU')
	txflines=txf.readlines()
	txf.close()
	for tl in txflines:
		tl=tl.strip()
		t=tl[:-1]
		#print t
		for p in puncts:
			if p in t:
				currentuglies.append(tl)
				#print tl
			else: pass
	if currentuglies:
		print '\n\n'+txfn
		for c in currentuglies:
			print c
