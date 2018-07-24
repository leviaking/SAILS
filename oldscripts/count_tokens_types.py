#!/usr/bin/env python

## 2015/10/20. LK.
###USAGE:
###python count_tokens_types.py directory
###"directory" here should be one of the highest level directories containing the pre-processed test or GS data. For now, these are NNSO, NNSLM, and GS; they all contain subfolders txt/, ldh/, etc.
###

import sys, os

home=sys.argv[1]
os.chdir(home)

subdirs = ['xdx', 'ldh', 'xdh', 'lxh', 'ldx'] ##NOTE that 'xdx' is serving as 'lemma' here; this is purely a matter of convenience, because we do not have proper lemma data in the same format as the other types
items = ['i01', 'i02', 'i03', 'i04', 'i05', 'i06', 'i07', 'i08', 'i09', 'i10']

for sd in subdirs:
	print sd
	os.chdir(sd)
	for path, dirs, files in os.walk("."):
		pass
	for item in items:
		tokens = []
		types = []
		for myfilename in files:
			if myfilename.startswith(item):
				myfile = open(myfilename, 'r')
				mytext = myfile.readlines()
				for myline in mytext:
					myline = myline.strip()
					myline = myline.split()
					myline = filter(None, myline)
					for t in myline:
						tokens.append(t)
						if t not in types:
							types.append(t)
		print len(tokens), '\t', len(types)
		#print '\n'
	# # print sd
	# # print files
	print "\n\n"
	os.chdir("..")
	