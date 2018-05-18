#!/usr/bin/env python

## 2015/07/13. LK. This script reads in a ONE-SENTENCE-PER-LINE text file and writes out an identical file (filename.txt.longfiltered) in which any sentence with more than 40 words has been removed.

import sys

textname=sys.argv[1]

newfile=open(textname+".longfiltered", 'w+')

#newsents=[]
with open(textname) as textfile:
	for tline in textfile:
		if len(tline.split()) <= 40:
			#newsents.append(tline)
			newfile.write(tline)
		else:
			pass

#with open(textname+".longfiltered") as newfile:
#	for n in newsents:
#		newfile.write(n)
