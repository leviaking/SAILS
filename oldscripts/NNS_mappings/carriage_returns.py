#!/usr/bin/env python

###9/21/2015. LK. For removing god damned carriage returns.

import sys, os

myopen = open(sys.argv[1], 'r')
myin = myopen.read()
myopen.close()
os.remove(sys.argv[1])
myout = myin.replace('\r', '\n')
outopen = open(sys.argv[1], 'w')
outopen.write(myout)
outopen.close()
