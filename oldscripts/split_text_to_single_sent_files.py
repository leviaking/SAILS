#!/usr/bin/env python

## 2015/08/16. LK. I have files that contain 1 sentence per line. I need to split each file into smaller files, each containing only one sentence.

import sys

infile=open(sys.argv[1], 'r')
prefix=sys.argv[2]
insents=infile.readlines()
insents=filter(None, insents)
counter=1
for sent in insents:
	counterstring=str(counter).zfill(2)
	outname=prefix+counterstring+'.txt'
	outfile=open(outname, 'w')
	outfile.write(sent)
	outfile.close()
	counter+=1