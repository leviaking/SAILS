#!/usr/bin/env python

##This script takes the agreement files and outputs a single csv with many different agreement measures. This includes agreement scores per item per feature, but also averages per item, and per feature, and for targeted/untargeted.


import sys, re, csv, datetime, os
from shutil import copyfile

hour = '2039'

##csvU is unsorted, csvS is sorted

feats=['Answer', 'Core', 'Gramm', 'Interp', 'Verif']
tuversions = ['T', 'U']

allfns=[]
allstatsdict={}
for num in range(1,4):
	numstr=str(num).zfill(2)
	for feat in feats:
		for tu in tuversions:
			fn='agreesecondpassanno_I'+numstr+tu+'_'+feat+'-2039.csv'
			allfns.append(fn)
			myf=open(fn, 'r')
			myfreader=csv.reader(myf, dialect=csv.excel)
			skipheader=next(myfreader, None)
			myfagrees=0
			myfdisagrees=0
			for myfrow in myfreader:
				z=myfrow[3]
				if z.strip()=='1':
					myfagrees+=1
				if z.strip()=='0':
					myfdisagrees+=1
				else:
					pass
				myftotal=myfagrees+myfdisagrees
				myfagreement=float(myfagrees)/float(myftotal)
				allstatsdict[fn]=['I'+numstr+tu+'_'+feat, myfagrees, myfdisagrees, myftotal, str(myfagreement)]

allfns.sort()
outheader=['File or Set', 'Agree Resp', 'Disagree Resp', 'Total Resp', 'Agreement']
outrows=[outheader]
for fn in allfns:
	outrows.append(allstatsdict[fn])

for feat in feats:
	for tu in tuversions:
		#ftrow=[]
		fta=0
		ftd=0
		ftt=0
		for fn in allfns:
			if feat in fn and tu in fn:
				info=allstatsdict[fn]
				fta+=info[1]
				ftd+=info[2]
				ftt+=info[3]
		ftagreement=float(fta)/float(ftt)
		ftrow=[feat+'_'+tu, fta, ftd, ftt, ftagreement]
		outrows.append(ftrow)

for feat in feats:
	fa=0
	fd=0
	ft=0
	for fn in allfns:
		if feat in fn:
			info=allstatsdict[fn]
			fa+=info[1]
			fd+=info[2]
			ft+=info[3]
	fagreement=float(fa)/float(ft)
	featrow=[feat, fa, fd, ft, fagreement]
	outrows.append(featrow)
	
for tu in tuversions:
	ta=0
	td=0
	tt=0
	for fn in allfns:
		if tu in fn:
			info=allstatsdict[fn]
			ta+=info[1]
			td+=info[2]
			tt+=info[3]
	tagreement=float(ta)/float(tt)
	turow=[tu, ta, td, tt, tagreement]
	outrows.append(turow)

statsname='agreement_stats_output.csv'
statsfile=open(statsname, 'w')
statswriter=csv.writer(statsfile, dialect=csv.excel)
for c in outrows:
	statswriter.writerow(c)
statsfile.close()
