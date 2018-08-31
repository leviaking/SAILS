#!/usr/bin/env python

##LK 

# import sys, re, csv, datetime, os
# from shutil import copyfile
# allrows=['0', '1', '2', '3', '5', '6', '7', '8']
# ci=0
# while ci < len(allrows):
# 	print 'test'+' '+allrows[ci]
# 	print 'GSa '+' '.join(allrows[:ci])
# 	print 'GSb '+' '.join(allrows[int(ci)+1:])
# 	ci+=1

everything = [['a', 'b', 'c'], ['e', 'f', 'g'], ['h', 'i', 'j']]

nums=[['1'], ['2'], ['3']]
romans=['I', 'II', 'III']
mega=zip(everything, nums, romans)
print mega