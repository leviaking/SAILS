#!/usr/bin/env python

##LK: Note that any CSV files produced in Excel must be saved as WINDOWS csv in Excel in order to work smoothly with this script!

import sys, re, csv

trowdict = {}
urowdict = {}
ckeylist=[]
with open('targeted_master.csv', 'r') as rawtargeted:
	rawtargetedreader = csv.reader(rawtargeted)
	theader = next(rawtargetedreader, None)
	for trow in rawtargetedreader:
		tkey = trow[0]
		if tkey not in trowdict:
			trowdict[tkey]=trow
		if tkey not in ckeylist:
			ckeylist.append(tkey)

with open('untargeted_master.csv', 'r') as rawuntargeted:
	rawuntargetedreader = csv.reader(rawuntargeted)
	uheader = next(rawuntargetedreader, None)
	for urow in rawuntargetedreader:
		ukey = urow[0]
		if ukey not in urowdict:
			urowdict[ukey]=urow
		if ukey not in ckeylist:
			ckeylist.append(ukey)

ukeep = uheader[11:]
#print ukeep
cheader = theader+ukeep
#print len(cheader)
#print cheader

clist = []

for ckey in ckeylist:
	if ckey in trowdict:
		crowq = trowdict[ckey][:11] ## "q" for questionnaire section
		#print crowq
		crowt = trowdict[ckey][11:]
		#print len(crowt), crowt
		if ckey in urowdict:
			crowu = urowdict[ckey][11:]
		else:
			crowu = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
	else:
		crowq = urowdict[ckey][:11]
		crowt = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
		crowu = urowdict[ckey][11:]
	crowfull = crowq+crowt+crowu
	clist.append(crowfull)
clist.sort()
clist.insert(0, cheader)
#print clist

with open('combined_master.csv', 'wb') as cfile:
	cwriter = csv.writer(cfile)
	for c in clist:
		cwriter.writerow(c)
		
		

#print ckeylist
#print theader

# nnslist = nnsfile.read().split('\n')
# for nns in nnslist:
# 	nns = re.sub('\.$', '', nns)
# 	if nns in typecount:
# 		typecount[nns]+=1
# 	else:
# 		typecount[nns]=1
# 
# print "number of types: "+str(len(typecount))+"\n\n"
# for tc in typecount:
# 	print tc+"\t"+str(typecount[tc])
