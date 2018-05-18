#!/usr/bin/env python

## 09/24/2014. LK. Use this script to lowercase and tokenize original NNS sentences. We need them in this form so we can compare them to the sentenences selected by the "Corrector" module (aspell/LM), which have undergone lowering and tokenization.

## USAGE: python token_and_lower.py inputfile

import sys
from nltk.tokenize import word_tokenize

inputname=sys.argv[1]
inputfile=open(inputname, 'r')
mystring=inputfile.read().strip()

def token_and_lower(list_as_string):
	az=list_as_string.split('\n')
	az=filter(None, az)
	yz=[]
	for bz in az:
		bz=bz.lower()
		cz=word_tokenize(bz)
		dz=' '.join(cz)
		dz=dz.strip()
		yz.append(dz)
	zz='\n'.join(yz)
	return zz

z = token_and_lower(mystring)
print z
print '\n'
outputname=inputname+'.tl'
outputfile=open(outputname, 'w')
outputfile.write(z)
outputfile.close()