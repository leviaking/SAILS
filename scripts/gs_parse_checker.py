#!/usr/bin/env python

## 2018/07/05. LK. 

import sys, re, csv, datetime, os
from shutil import copyfile

print ' '.join(['file_id', 'csvcount', 'txtcount', 'lxcount', 'pcount', 'lkcount', 'lccount', 'fincount'])

csvdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/rawcsvs/')
lcdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemma_conll/')
lkconlldir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/LKconll/')
penndir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/penn/')
txtdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/txt/')
lemmaxmldir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemmaxml/')
findir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/finalcsvs/')

def get_all_lemma_conll_filenames(): ##this will get a list of all the files in the lemma_conll directory; these are the files that were fully processed.
	for stuff in os.walk('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemma_conll/'):
		mystuff=stuff[2]
		return mystuff
	
def check_file_lengths(lcfilenames):
	matching=[]
	nonmatching=[]
	for lcfn in lcfilenames: ##lcfn for lemma_conll file
		file_id=lcfn.split('.')[0]
		##get original csv count
		csvfn= file_id+'.csv'
		csvf=open(csvdir+csvfn, 'rU')
		mycsvreader=csv.reader(csvf, dialect=csv.excel)
		skip_header=next(mycsvreader, None)
		csvcount=0
		for row in mycsvreader:
			csvcount+=1
		csvf.close()
		##get lemma_conll count
		lcf=open(lcdir+lcfn, 'rU')
		lccount=0
		for l in lcf.readlines():
			if not l.strip():
				lccount+=1
		lcf.close()
		##get lkconll count
		lkfn=file_id+'.LKconll'
		lkf=open(lkconlldir+lkfn, 'rU')
		lkcount=0
		for lk in lkf.readlines():
			if not lk.strip():
				lkcount+=1
		lkf.close()
		##get penn count
		pfn=file_id+'.penn'
		pf=open(penndir+pfn, 'rU')
		pcount=0
		for p in pf.readlines():
			if not p.strip():
				pcount+=1
		pf.close()
		##get txt count
		txtfn=file_id+'.txt'
		txtf=open(txtdir+txtfn, 'rU')
		txtlines=txtf.readlines()
		filter(None, txtlines)
		txtcount=len(txtlines)
		##get lemmaxml count
		#<sentence id="1">
		lxfn=file_id+'.xml'
		lxf=open(lemmaxmldir+lxfn, 'rU')
		lxlines=lxf.readlines()
		lxcount=0
		for lxline in lxlines:
			if lxline.strip()=='''<sentence id="1">''':
				lxcount+=1
			else: pass
		##get finalcsv count
		finfn= file_id+'.csv'
		finf=open(findir+finfn, 'rU')
		finreader=csv.reader(finf, dialect=csv.excel)
		skip_header=next(finreader, None)
		fincount=0
		for row in finreader:
			fincount+=1
		finf.close()
		##check for matching counts; order here copies the order the files are produced via the shell: csvcount, txtcount, lxcount, pcount, lkcount, lccount
		integercounts={'csvcount':csvcount, 'txtcount':txtcount, 'lxcount':lxcount, 'pcount':pcount, 'lkcount':lkcount, 'lccount':lccount, 'fincount':fincount}
		orderlist=['csvcount', 'txtcount', 'lxcount', 'pcount', 'lkcount', 'lccount', 'fincount']
		stringdict={}
		for o in orderlist:
			stringdict[o]=str(integercounts[o])
		if stringdict['csvcount']==stringdict['txtcount']==stringdict['lxcount']==stringdict['pcount']==stringdict['lkcount']==stringdict['lccount']==stringdict['fincount']:
			matching.append([file_id, stringdict['csvcount'], stringdict['txtcount'], stringdict['lxcount'], stringdict['pcount'], stringdict['lkcount'], stringdict['lccount'], stringdict['fincount']])
		else:
			nonmatching.append([file_id, stringdict['csvcount'], stringdict['txtcount'], stringdict['lxcount'], stringdict['pcount'], stringdict['lkcount'], stringdict['lccount'], stringdict['fincount']])
		#print file_id+'\t'+str(csvcount)+'\t'+str(lccount)+'\n'
	print 'Non-Matches:'
	for nm in nonmatching:
		print '\t'.join(nm)
		
	print '\nMatches:'
	for m in matching:
		print '\t'.join(m)
	return nonmatching

def show_responses(nm): ## i want this function to go through the non-matching cases and show response by response, the txt and lemma_conll, so I can find where the mismatch begins.
	for n in nm:
		file_id=n[0]
		print '\n'+file_id
		txtfn=file_id+'.txt'
		txtf=open(txtdir+txtfn, 'rU')
		txtsents=txtf.readlines()
		filter(None, txtsents)
		lcfn=file_id+'.lemma_conll'
		lcf=open(lcdir+lcfn, 'rU')
		lcfull=lcf.read()
		#print lcfull
		lcsents=lcfull.split('\n\n')
		filter(None, lcsents)
		#print lcsents
		count=1
		while txtsents or lcsents:
			try:
				t=txtsents.pop(0)
			except:
				t='EMPTY (txt)'
			try:
				lcurrent=lcsents.pop(0)
				lcurrent=lcurrent.split('\n')
			except:
				l='No LC to pop'
			try:
				ls=[]
				for row in lcurrent:
					#print row
					word=row.split('\t')[1]
					#print word
					ls.append(word)
					l=' '.join(ls)
			except:
				l='EMPTY (lemma_conll)'
			print str(count)+'\t'+t.strip()+'\n'+str(count)+'\t'+l.strip()+'\n'
			count+=1
		print '\n\n'


#check_file_lengths()
myfiles=get_all_lemma_conll_filenames()
all_ns=[]
for myf in myfiles:
	if "all_ns" in myf:
		all_ns.append(myf)
	else: pass
all_ns.sort()
nonmatching=check_file_lengths(all_ns)
show_responses(nonmatching)