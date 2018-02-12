#!/usr/bin/env python

##This script takes the agreement files and outputs a single csv with many different agreement measures. This includes agreement scores per item per feature, but also averages per item, and per feature, and for targeted/untargeted.


import sys, re, csv, datetime, os
from shutil import copyfile


feats=[
	'Core',
	'Answer',
	'Gramm',
	'Interp',
	'Verif'
	]
featcoldict={'Core': 13, 'Answer': 14, 'Gramm': 15, 'Interp': 16, 'Verif': 17}
tuversions = ['T', 'U']

# debugfile=open('debug.csv', 'w')
# debugwriter=csv.writer(debugfile, dialect=csv.excel)
# debugrows=[['file', 'missing anno']]

allfns=[]
allstatsdict={}
allagrees={}
alldisagrees={}
for num in range(1,4):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		myfilename='I'+numstr+tu+'_master_anno.csv'
		myfile=open(myfilename, 'r')
		myfreader=csv.reader(myfile, dialect=csv.excel)
		skipheader=next(myfreader, None)
		myfrows=[]
		for m in myfreader:
			myfrows.append(m)
##rows in myfrows look like this:
##(HEADER ROW)##RespondentID	Purchased response?	Source	L1 Eng?	L1s	Other Ls	Country	Age	Gender	years Eng	Eng residence	1stOr2ndResponse	What is the boy doing?	A1 Core	A1 Answer	A1 Gramm	A1 Interp	A1 Verif	A2 Core	A2 Answer	A2 Gramm	A2 Interp	A2 Verif
		myfile.close()
		for feat in feats:
			fn='I'+numstr+tu+'_'+feat
			allfns.append(fn)
			A1yes=0.0
			A1no=0.0
			A2yes=0.0
			A2no=0.0
			myfagrees=0.0
			myfdisagrees=0.0
			missedanno=0.0
			ftagrees=[]
			ftdisagrees=[]
			for myfrow in myfrows:
				resp=myfrow[12]
				if resp=='0':
					pass
				else:
					try:
						A2=myfrow[featcoldict[feat]+5]
					except:
						print 'EXCEPTION'
						missedanno+=1
						pass
					A1anno=myfrow[featcoldict[feat]]
					A2anno=myfrow[featcoldict[feat]+5]
					if A1anno.strip()=='1':
						A1yes+=1
					else:
						A1no+=1
					if A2anno.strip()=='1':
						A2yes+=1
					else:
						A2no+=1
					if A1anno==A2anno:
						myfagrees+=1
						ftagrees.append([resp, A1anno, A2anno])
					else:
						myfdisagrees+=1
						ftdisagrees.append([resp, A1anno, A2anno])
			allagrees[fn]=ftagrees
			alldisagrees[fn]=ftdisagrees
			myftotal=myfagrees+myfdisagrees
			# print myftotal
			# print fn
			try:
				yeschance=float(A1yes/myftotal)*float(A2yes/myftotal)
				#print 'yeschance', yeschance
			except: yeschance='NA'
			try:
				nochance=float(A1no/myftotal)*float(A2no/myftotal)
				#print 'nochance', nochance
			except: nochance='NA'
			try:
				allchance=float(yeschance+nochance)
				#print 'allchance', allchance
			except: allchance='NA'
			try:
				pagree=float(myfagrees/myftotal)
				pdisagree=float(myfdisagrees/myftotal)
				kappa=float(pagree-allchance)/float(1-allchance)
				A1yesp=float(A1yes/myftotal)
				A1nop=float(A1no/myftotal)
				A2yesp=float(A2yes/myftotal)
				A2nop=float(A2no/myftotal)
				yeschanceagree=float(A1yesp*A2yesp)
				nochanceagree=float(A1nop*A2nop)
				chanceagree=float(yeschanceagree+nochanceagree)
				#print 'kappa', kappa
			except:
				pagree='NA'
				pdisagree='NA'
				kappa='NA'
				A1yesp='NA'
				A1nop='NA'
				A2yesp='NA'
				A2nop='NA'
				yeschanceagree='NA'
				nochanceagree='NA'
				chanceagree='NA'
				#print 'kappa fail'
			allstatsdict[fn]=[fn, myfagrees, pagree, myfdisagrees, pdisagree, myftotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]

allfns.sort()
outheader=['File or Set', 'Agree Resp', 'Agree %', 'Disagree Resp', 'Disagree %', 'Total Resp', 'Kappa', 'A1yes', 'A1yes %', 'A1no', 'A1no %', 'A2yes', 'A2yes %', 'A2no', 'A2no %', 'Yes chance agree', 'No chance agree', 'Chance agree']
outrows=[outheader]

##item+TU+feat
for fn in allfns:
	outrows.append(allstatsdict[fn])

##item+TU
for num in range(1,4):
	numstr=str(num).zfill(2)
	for tu in tuversions:
		A1yes=0
		A1no=0
		A2yes=0
		A2no=0
		myagrees=0
		mydisagrees=0
		for fn in allfns:
			if numstr in fn and tu in fn:
				info=allstatsdict[fn]
				A1yes+=info[7]
				A1no+=info[8]
				A2yes+=info[9]
				A2no+=info[10]
				myagrees+=info[1]
				mydisagrees+=info[2]
		mytotal=myagrees+mydisagrees
		try:
			yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
		except: yeschance='NA'
		try:
			nochance=float(A1no/mytotal)*float(A2no/mytotal)
		except: nochance='NA'
		try:
			allchance=float(yeschance+nochance)
		except: allchance='NA'
		try:
			pagree=float(myagrees/mytotal)
			pdisagree=float(mydisagrees/mytotal)
			kappa=float(pagree-allchance)/float(1-allchance)
			A1yesp=float(A1yes/mytotal)
			A1nop=float(A1no/mytotal)
			A2yesp=float(A2yes/mytotal)
			A2nop=float(A2no/mytotal)
			yeschanceagree=float(A1yesp*A2yesp)
			nochanceagree=float(A1nop*A2nop)
			chanceagree=float(yeschanceagree+nochanceagree)
			#print 'kappa', kappa
		except:
			pagree='NA'
			pdisagree='NA'
			kappa='NA'
			A1yesp='NA'
			A1nop='NA'
			A2yesp='NA'
			A2nop='NA'
			yeschanceagree='NA'
			nochanceagree='NA'
			chanceagree='NA'
			#print 'kappa fail'
		ftrow=['I'+numstr+tu, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
		outrows.append(ftrow)
		
##item+feat
for num in range(1,4):
	numstr=str(num).zfill(2)
	for feat in feats:
		A1yes=0
		A1no=0
		A2yes=0
		A2no=0
		myagrees=0
		mydisagrees=0
		for fn in allfns:
			if numstr in fn and feat in fn:
				info=allstatsdict[fn]
				A1yes+=info[7]
				A1no+=info[8]
				A2yes+=info[9]
				A2no+=info[10]
				myagrees+=info[1]
				mydisagrees+=info[2]
		mytotal=myagrees+mydisagrees
		try:
			yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
		except: yeschance='NA'
		try:
			nochance=float(A1no/mytotal)*float(A2no/mytotal)
		except: nochance='NA'
		try:
			allchance=float(yeschance+nochance)
		except: allchance='NA'
		try:
			pagree=float(myagrees/mytotal)
			pdisagree=float(mydisagrees/mytotal)
			kappa=float(pagree-allchance)/float(1-allchance)
			A1yesp=float(A1yes/mytotal)
			A1nop=float(A1no/mytotal)
			A2yesp=float(A2yes/mytotal)
			A2nop=float(A2no/mytotal)
			yeschanceagree=float(A1yesp*A2yesp)
			nochanceagree=float(A1nop*A2nop)
			chanceagree=float(yeschanceagree+nochanceagree)
			#print 'kappa', kappa
		except:
			pagree='NA'
			pdisagree='NA'
			kappa='NA'
			A1yesp='NA'
			A1nop='NA'
			A2yesp='NA'
			A2nop='NA'
			yeschanceagree='NA'
			nochanceagree='NA'
			chanceagree='NA'
			#print 'kappa fail'
		ftrow=['I'+numstr+feat, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
		outrows.append(ftrow)

##feat+TU
for feat in feats:
	for tu in tuversions:
		# outheader=['File or Set', 'Agree Resp', 'Disagree Resp', 'Total Resp', 'Kappa', 'A1yes', 'A1no', 'A2yes', 'A2no']
		A1yes=0
		A1no=0
		A2yes=0
		A2no=0
		myagrees=0
		mydisagrees=0
		for fn in allfns:
			if feat in fn and tu in fn:
				info=allstatsdict[fn]
				A1yes+=info[7]
				A1no+=info[8]
				A2yes+=info[9]
				A2no+=info[10]
				myagrees+=info[1]
				mydisagrees+=info[2]
		mytotal=myagrees+mydisagrees
		try:
			yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
		except: yeschance='NA'
		try:
			nochance=float(A1no/mytotal)*float(A2no/mytotal)
		except: nochance='NA'
		try:
			allchance=float(yeschance+nochance)
		except: allchance='NA'
		try:
			pagree=float(myagrees/mytotal)
			pdisagree=float(mydisagrees/mytotal)
			kappa=float(pagree-allchance)/float(1-allchance)
			A1yesp=float(A1yes/mytotal)
			A1nop=float(A1no/mytotal)
			A2yesp=float(A2yes/mytotal)
			A2nop=float(A2no/mytotal)
			yeschanceagree=float(A1yesp*A2yesp)
			nochanceagree=float(A1nop*A2nop)
			chanceagree=float(yeschanceagree+nochanceagree)
			#print 'kappa', kappa
		except:
			pagree='NA'
			pdisagree='NA'
			kappa='NA'
			A1yesp='NA'
			A1nop='NA'
			A2yesp='NA'
			A2nop='NA'
			yeschanceagree='NA'
			nochanceagree='NA'
			chanceagree='NA'
			#print 'kappa fail'
		ftrow=[feat+'_'+tu, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
		outrows.append(ftrow)

##item
for num in range(1,4):
	numstr=str(num).zfill(2)
	A1yes=0
	A1no=0
	A2yes=0
	A2no=0
	myagrees=0
	mydisagrees=0
	for fn in allfns:
		if numstr in fn:
			info=allstatsdict[fn]
			A1yes+=info[7]
			A1no+=info[8]
			A2yes+=info[9]
			A2no+=info[10]
			myagrees+=info[1]
			mydisagrees+=info[2]
	mytotal=myagrees+mydisagrees
	try:
		yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
	except: yeschance='NA'
	try:
		nochance=float(A1no/mytotal)*float(A2no/mytotal)
	except: nochance='NA'
	try:
		allchance=float(yeschance+nochance)
	except: allchance='NA'
	try:
		pagree=float(myagrees/mytotal)
		pdisagree=float(mydisagrees/mytotal)
		kappa=float(pagree-allchance)/float(1-allchance)
		A1yesp=float(A1yes/mytotal)
		A1nop=float(A1no/mytotal)
		A2yesp=float(A2yes/mytotal)
		A2nop=float(A2no/mytotal)
		yeschanceagree=float(A1yesp*A2yesp)
		nochanceagree=float(A1nop*A2nop)
		chanceagree=float(yeschanceagree+nochanceagree)
		#print 'kappa', kappa
	except:
		pagree='NA'
		pdisagree='NA'
		kappa='NA'
		A1yesp='NA'
		A1nop='NA'
		A2yesp='NA'
		A2nop='NA'
		yeschanceagree='NA'
		nochanceagree='NA'
		chanceagree='NA'
		#print 'kappa fail'
	ftrow=['I'+numstr, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
	outrows.append(ftrow)	

##feat
for feat in feats:
	A1yes=0
	A1no=0
	A2yes=0
	A2no=0
	myagrees=0
	mydisagrees=0
	for fn in allfns:
		if feat in fn:
			info=allstatsdict[fn]
			A1yes+=info[7]
			A1no+=info[8]
			A2yes+=info[9]
			A2no+=info[10]
			myagrees+=info[1]
			mydisagrees+=info[2]
	mytotal=myagrees+mydisagrees
	try:
		yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
	except: yeschance='NA'
	try:
		nochance=float(A1no/mytotal)*float(A2no/mytotal)
	except: nochance='NA'
	try:
		allchance=float(yeschance+nochance)
	except: allchance='NA'
	try:
		pagree=float(myagrees/mytotal)
		pdisagree=float(mydisagrees/mytotal)
		kappa=float(pagree-allchance)/float(1-allchance)
		A1yesp=float(A1yes/mytotal)
		A1nop=float(A1no/mytotal)
		A2yesp=float(A2yes/mytotal)
		A2nop=float(A2no/mytotal)
		yeschanceagree=float(A1yesp*A2yesp)
		nochanceagree=float(A1nop*A2nop)
		chanceagree=float(yeschanceagree+nochanceagree)
		#print 'kappa', kappa
	except:
		pagree='NA'
		pdisagree='NA'
		kappa='NA'
		A1yesp='NA'
		A1nop='NA'
		A2yesp='NA'
		A2nop='NA'
		yeschanceagree='NA'
		nochanceagree='NA'
		chanceagree='NA'
		#print 'kappa fail'
	ftrow=[feat, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
	outrows.append(ftrow)

##TU
for tu in tuversions:
	A1yes=0
	A1no=0
	A2yes=0
	A2no=0
	myagrees=0
	mydisagrees=0
	for fn in allfns:
		if tu in fn:
			info=allstatsdict[fn]
			A1yes+=info[7]
			A1no+=info[8]
			A2yes+=info[9]
			A2no+=info[10]
			myagrees+=info[1]
			mydisagrees+=info[2]
	mytotal=myagrees+mydisagrees
	try:
		yeschance=float(A1yes/mytotal)*float(A2yes/mytotal)
	except: yeschance='NA'
	try:
		nochance=float(A1no/mytotal)*float(A2no/mytotal)
	except: nochance='NA'
	try:
		allchance=float(yeschance+nochance)
	except: allchance='NA'
	try:
		pagree=float(myagrees/mytotal)
		pdisagree=float(mydisagrees/mytotal)
		kappa=float(pagree-allchance)/float(1-allchance)
		A1yesp=float(A1yes/mytotal)
		A1nop=float(A1no/mytotal)
		A2yesp=float(A2yes/mytotal)
		A2nop=float(A2no/mytotal)
		yeschanceagree=float(A1yesp*A2yesp)
		nochanceagree=float(A1nop*A2nop)
		chanceagree=float(yeschanceagree+nochanceagree)
		#print 'kappa', kappa
	except:
		pagree='NA'
		pdisagree='NA'
		kappa='NA'
		A1yesp='NA'
		A1nop='NA'
		A2yesp='NA'
		A2nop='NA'
		yeschanceagree='NA'
		nochanceagree='NA'
		chanceagree='NA'
		#print 'kappa fail'
	ftrow=[tu, myagrees, pagree, mydisagrees, pdisagree, mytotal, kappa, A1yes, A1yesp, A1no, A1nop, A2yes, A2yesp, A2no, A2nop, yeschanceagree, nochanceagree, chanceagree]
	outrows.append(ftrow)

###This section is for writing out agree responses to a csv file, and disagree responses to another csv file. We do this for various groupings/granularity of the data.
header=['Source', 'Response', 'A1', 'A2']
##items+TU+feature
##item+TU
##item+feature
##TU+feature
##items
##TU
##feature

##items+TU+feature
for fn in allfns:
	fnagreesfile=open('agreement_files/'+fn+'_token_agrees.csv', 'w')
	fndisagreesfile=open('agreement_files/'+fn+'_token_disagrees.csv', 'w')
	fnagreeswriter=csv.writer(fnagreesfile, dialect=csv.excel)
	fndisagreeswriter=csv.writer(fndisagreesfile, dialect=csv.excel)
	fnagreeswriter.writerow(header)
	fndisagreeswriter.writerow(header)
	fnagrees=allagrees[fn]
	fndisagrees=alldisagrees[fn]
	for a in fnagrees:
		fnagreeswriter.writerow([fn]+a)
	for d in fndisagrees:
		fndisagreeswriter.writerow([fn]+d)
	fnagreesfile.close()
	fndisagreesfile.close()

##item+TU
for n in range(1,4):
	numstr=str(n).zfill(2)
	for tu in tuversions:
		itemtuagreesfile=open('agreement_files/'+numstr+tu+'_token_agrees.csv', 'w')
		itemtuagreeswriter=csv.writer(itemtuagreesfile, dialect=csv.excel)
		itemtuagreeswriter.writerow(header)
		itemtudisagreesfile=open('agreement_files/'+numstr+tu+'_token_disagrees.csv', 'w')
		itemtudisagreeswriter=csv.writer(itemtudisagreesfile, dialect=csv.excel)
		itemtudisagreeswriter.writerow(header)
		for fn in allfns:
			if numstr in fn and tu in fn:
				itemtuagrees=allagrees[fn]
				itemtudisagrees=alldisagrees[fn]
				for r in itemtuagrees:
					itemtuagreeswriter.writerow([fn]+r)
				for d in itemtudisagrees:
					itemtudisagreeswriter.writerow([fn]+d)
		itemtuagreesfile.close()
		itemtudisagreesfile.close()

##item+features
for n in range(1,4):
	numstr=str(n).zfill(2)
	for feat in feats:
		itemfeatagreesfile=open('agreement_files/'+numstr+feat+'_token_agrees.csv', 'w')
		itemfeatagreeswriter=csv.writer(itemfeatagreesfile, dialect=csv.excel)
		itemfeatagreeswriter.writerow(header)
		itemfeatdisagreesfile=open('agreement_files/'+numstr+feat+'_token_disagrees.csv', 'w')
		itemfeatdisagreeswriter=csv.writer(itemfeatdisagreesfile, dialect=csv.excel)
		itemfeatdisagreeswriter.writerow(header)
		for fn in allfns:
			if feat in fn and numstr in fn:
				itemfeatagrees=allagrees[fn]
				itemfeatdisagrees=alldisagrees[fn]
				for r in itemfeatagrees:
					itemfeatagreeswriter.writerow([fn]+r)
				for d in itemfeatdisagrees:
					itemfeatdisagreeswriter.writerow([fn]+d)
		itemfeatagreesfile.close()
		itemfeatdisagreesfile.close()

##TU+features
for tu in tuversions:
	for feat in feats:
		feattuagreesfile=open('agreement_files/'+tu+'_'+feat+'_token_agrees.csv', 'w')
		feattuagreeswriter=csv.writer(feattuagreesfile, dialect=csv.excel)
		feattuagreeswriter.writerow(header)
		feattudisagreesfile=open('agreement_files/'+tu+'_'+feat+'_token_disagrees.csv', 'w')
		feattudisagreeswriter=csv.writer(feattudisagreesfile, dialect=csv.excel)
		feattudisagreeswriter.writerow(header)
		for fn in allfns:
			if feat in fn and tu in fn:
				feattuagrees=allagrees[fn]
				feattudisagrees=alldisagrees[fn]
				for r in feattuagrees:
					feattuagreeswriter.writerow([fn]+r)
				for d in feattudisagrees:
					feattudisagreeswriter.writerow([fn]+d)
		feattuagreesfile.close()
		feattudisagreesfile.close()

##item
for n in range(1,4):
	numstr=str(n).zfill(2)
	itemfeatagreesfile=open('agreement_files/'+numstr+'_token_agrees.csv', 'w')
	itemfeatagreeswriter=csv.writer(itemfeatagreesfile, dialect=csv.excel)
	itemfeatagreeswriter.writerow(header)
	itemfeatdisagreesfile=open('agreement_files/'+numstr+'_token_disagrees.csv', 'w')
	itemfeatdisagreeswriter=csv.writer(itemfeatdisagreesfile, dialect=csv.excel)
	itemfeatdisagreeswriter.writerow(header)
	for fn in allfns:
		if numstr in fn:
			itemfeatagrees=allagrees[fn]
			itemfeatdisagrees=alldisagrees[fn]
			for r in itemfeatagrees:
				itemfeatagreeswriter.writerow([fn]+r)
			for d in itemfeatdisagrees:
				itemfeatdisagreeswriter.writerow([fn]+d)
	itemfeatagreesfile.close()
	itemfeatdisagreesfile.close()


##TU (targeted vs untargeted)
for tu in tuversions:
	tuagreesfile=open('agreement_files/'+tu+'_token_agrees.csv', 'w')
	tuagreeswriter=csv.writer(tuagreesfile, dialect=csv.excel)
	tuagreeswriter.writerow(header)
	tudisagreesfile=open('agreement_files/'+tu+'_token_disagrees.csv', 'w')
	tudisagreeswriter=csv.writer(tudisagreesfile, dialect=csv.excel)
	tudisagreeswriter.writerow(header)
	for fn in allfns:
		if tu in fn:
			tuagrees=allagrees[fn]
			tudisagrees=alldisagrees[fn]
			for r in tuagrees:
				tuagreeswriter.writerow([fn]+r)
			for d in tudisagrees:
				tudisagreeswriter.writerow([fn]+d)
	tuagreesfile.close()
	tudisagreesfile.close()

##features
for feat in feats:
	featagreesfile=open('agreement_files/'+feat+'_token_agrees.csv', 'w')
	featagreeswriter=csv.writer(featagreesfile, dialect=csv.excel)
	featagreeswriter.writerow(header)
	featdisagreesfile=open('agreement_files/'+feat+'_token_disagrees.csv', 'w')
	featdisagreeswriter=csv.writer(featdisagreesfile, dialect=csv.excel)
	featdisagreeswriter.writerow(header)
	for fn in allfns:
		if feat in fn:
			featagrees=allagrees[fn]
			featdisagrees=alldisagrees[fn]
			for r in featagrees:
				featagreeswriter.writerow([fn]+r)
			for d in featdisagrees:
				featdisagreeswriter.writerow([fn]+d)
	featagreesfile.close()
	featdisagreesfile.close()


	
statsname='token_agreement_stats_output.csv'
#statsfile=open('agreement_stats/'+statsname, 'w')
statsfile=open(statsname, 'w')
statswriter=csv.writer(statsfile, dialect=csv.excel)
#print outrows
for c in outrows:
	statswriter.writerow(c)
statsfile.close()
