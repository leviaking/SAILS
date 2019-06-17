#!/usr/bin/env python

##This script takes the annotation files and outputs a single csv with many different agreement measures. This includes agreement scores per item per feature, but also averages per item, and per feature, and for targeted/untargeted.


import sys, re, csv, datetime, os
from shutil import copyfile

intrans=['01', '04', '07', '10', '13', '18', '20', '24', '27', '30']
trans=['02', '06', '09', '12', '15', '16', '19', '22', '25', '29']
ditrans=['03', '05', '08', '11', '14', '17', '21', '23', '26', '28']

NNS=[
	'NSv1pt1',
	'NSv1pt2',
	'NSv2pt1',
	'NSv2pt2',
	'NSv1',
	'NSv2'
	]

NS=[
	'NNSv1',
	'NNSv2'
	]

Familars=[
	'NSv1',
	'NSv2'
	]

Crowds=[
	'NSv1pt1',
	'NSv1pt2',
	'NSv2pt1',
	'NSv2pt2'
	]

speakers={
	'L1':[
	'NSv1pt1',
	'NSv1pt2',
	'NSv2pt1',
	'NSv2pt2',
	'NSv1',
	'NSv2'
		],
	'L2':[
	'NNSv1',
	'NNSv2'
		]
	}

feats=[
	'Core',
	'Answer',
	'Gramm',
	'Interp',
	'Verif'
	]

featcoldict={'Core': 13, 'Answer': 14, 'Gramm': 15, 'Interp': 16, 'Verif': 17}
tuversions = ['T', 'U']

allfns=[]
allstatsdict={}
allagrees={}
alldisagrees={}
for num in range(1,31):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		myfilename='I'+numstr+tu+'_master_anno.csv'
		myfile=open(myfilename, 'rU')
		myfreader=csv.reader(myfile, dialect=csv.excel)
		skipheader=next(myfreader, None)
		myfrows=[]
		for m in myfreader:
			myfrows.append(m)
##rows in myfrows look like this:
##(HEADER ROW)##RespondentID	Purchased response?	Source	L1 Eng?	L1s	Other Ls	Country	Age	Gender	years Eng	Eng residence	1stOr2ndResponse	What is the boy doing?	A1 Core	A1 Answer	A1 Gramm	A1 Interp	A1 Verif	A2 Core	A2 Answer	A2 Gramm	A2 Interp	A2 Verif
		myfile.close()
		for feat in feats:
			for speaker in speakers:
##03/13/2018 working below here:
				fn=speaker+'_I'+numstr+tu+'_'+feat
				allfns.append(fn)
				fnresps=[]
				for myfrow in myfrows:
					resp=myfrow[12]
					if resp.strip()=='0':
						pass
					else:
						currentspeaker=myfrow[2].strip()
						if currentspeaker in speakers[speaker]:
							fnresps.append(resp)
				allstatsdict[fn]=fnresps

allfns.sort()
print allfns

for speaker in speakers:
	respcount=0
	for fn in allfns:
		if speaker in fn and 'Core' in fn:
			respcount+=len(allstatsdict[fn])
	print speaker+': '+str(respcount)

for num in range(1,31):
	numstr=str(num).zfill(2)
	respcount=0
	for fn in allfns:
		if numstr in fn and 'Core' in fn:
			respcount+=len(allstatsdict[fn])
	print numstr+': '+str(respcount)

for num in range(1,31):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		respcount=0
		for fn in allfns:
			if numstr in fn and tu in fn and 'Core' in fn:
				respcount+=len(allstatsdict[fn])
		print numstr+'_'+tu+': '+str(respcount)
	
def write_resp_csv(setname):
	mysetfile=open(setname+'_responses.csv', 'w')
	respwriter=csv.writer(mysetfile, dialect=csv.excel)
	for fn in allfns:
		if setname in fn and 'Core' in fn:
			responses=allstatsdict[fn]
			for r in responses:
				respwriter.writerow([r])
	mysetfile.close()
	
for speaker in speakers:
	write_resp_csv(speaker)

for num in range(1,31):
	numstr=str(num).zfill(2)
	write_resp_csv(numstr)
	
for num in range(1,31):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		mysetfile=open(numstr+'_'+tu+'_responses.csv', 'w')
		respwriter=csv.writer(mysetfile, dialect=csv.excel)
		for fn in allfns:
			if numstr in fn and tu in fn and 'Core' in fn:
				responses=allstatsdict[fn]
				for r in responses:
					respwriter.writerow([r])
		mysetfile.close()
		
for num in range(1,31):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		for speaker in speakers:
			mysetfile=open(speaker+'_'+numstr+'_'+tu+'_responses.csv', 'w')
			respwriter=csv.writer(mysetfile, dialect=csv.excel)
			for fn in allfns:
				if numstr in fn and tu in fn and speaker in fn and 'Core' in fn:
					responses=allstatsdict[fn]
					for r in responses:
						respwriter.writerow([r])
			mysetfile.close()