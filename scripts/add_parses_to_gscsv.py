#!/usr/bin/env python

## 2018/07/15. LK. This script is to be run after the gscsv_to_lemmatized_conll.sh script (and after any problems have been found via gs_parse_checker.py and resolved). This script takes the lemma-parse from the *all_ns.lemma_conll file and adds it to a column of the csvs that were created via gs_assembler.py. These new files are saved in */final_csvs/.

import sys, re, csv, datetime, os
from shutil import copyfile

csvdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/rawcsvs/')
lcdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemma_conll/')
lkconlldir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/LKconll/')
penndir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/penn/')
txtdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/txt/')
lemmaxmldir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemmaxml/')
finaldir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/finalcsvs/')


def get_all_lemma_conll_filenames(): ##this will get a list of all the files in the lemma_conll directory; these are the files that were fully processed... when we run this, the only files in the lemma_conll folder should be the *all_ns.lemma_conll files, and these are the files that provide the parses that we apply to the other files.
	for stuff in os.walk('/Users/leviking/Documents/dissertation/SAILS/gold_standards/lemma_conll/'):
		mystuff=stuff[2]
	return mystuff

def get_handles(lcnames):
	hs=[]
	for lcn in lcnames:
		handle=lcn.split('.')[0]
		hs.append(handle)
	hs.sort()
	return hs
	

def copy_rawcsvs(handles): ##this copies the csvs (output by gs_assembler.py) from gold_standards/rawcsvs/ to gold_standards/final_csvs/.
	for handle in handles:
		copyfile(csvdir+handle+'.csv', finaldir+handle+'_lc.csv')

def get_parse_dict(h):
	hdict={}
	respids=[]
	idsource=open(csvdir+h+'.csv', 'rU')
	sreader=csv.reader(idsource, dialect=csv.excel)
	skipheader=next(sreader, None)
	for srow in sreader:
		respid=srow[0]
		respids.append(respid)
	idsource.close()
	parsesource=open(lcdir+h+'.lemma_conll', 'rU')
	parsefull=parsesource.read()
	parses=parsefull.split('\n\n')
	filter(None, parses)
	while respids:
		r=respids.pop(0)
		p=parses.pop(0)
		hdict[r]=p
	return hdict

def fill_csvs_with_parse(handle, pdict):
	item=handle.split('_')[0] ##e.g. 'I01T'
	##We also need to create:
	allns='_all_ns.csv'
	allfns='_all_fns.csv'
	allcns='_all_cns.csv'
	firsts='_firsts.csv'
	seconds='_seconds.csv'
	perfects='_perfects.csv'
	almosts='_almosts.csv'
	coreyes='_coreyes.csv'
	others=[allns, allfns, allcns, firsts, seconds, perfects, almosts, coreyes]
	for other in others:
		sourcerows=[]
		sourcepath=csvdir+item+other
		source=open(sourcepath, 'rU')
		sourcereader=csv.reader(source, dialect=csv.excel)
		fname=finaldir+item+other
		fin=open(fname, 'w')
		finwriter=csv.writer(fin, dialect=csv.excel)
		header=next(sourcereader, None)
		header=header+['parse']
		finwriter.writerow(header)
		for sourcerow in sourcereader:
			sourcerows.append(sourcerow)
		source.close()
		for sr in sourcerows:
			sr=filter(None, sr)
			if sr:
				rid=sr[0]
				parse=pdict[rid]
				#print parse
				#print rid
				finrow=sr+[parse]
				#print finrow
				finwriter.writerow(finrow)
			else:
				pass
		fin.close()
	

# def check_file_lengths(lcfilenames):
# 	matching=[]
# 	nonmatching=[]
# 	for lcfn in lcfilenames: ##lcfn for lemma_conll file
# 		file_id=lcfn.split('.')[0]
# 		##get original csv count
# 		csvfn= file_id+'.csv'
# 		csvf=open(csvdir+csvfn, 'rU')
# 		mycsvreader=csv.reader(csvf, dialect=csv.excel)
# 		skip_header=next(mycsvreader, None)
# 		csvcount=0
# 		for row in mycsvreader:
# 			csvcount+=1
# 		csvf.close()
# 		##get lemma_conll count
# 		lcf=open(lcdir+lcfn, 'rU')
# 		lccount=0
# 		for l in lcf.readlines():
# 			if not l.strip():
# 				lccount+=1
# 		lcf.close()
# 		##get lkconll count
# 		lkfn=file_id+'.LKconll'
# 		lkf=open(lkconlldir+lkfn, 'rU')
# 		lkcount=0
# 		for lk in lkf.readlines():
# 			if not lk.strip():
# 				lkcount+=1
# 		lkf.close()
# 		##get penn count
# 		pfn=file_id+'.penn'
# 		pf=open(penndir+pfn, 'rU')
# 		pcount=0
# 		for p in pf.readlines():
# 			if not p.strip():
# 				pcount+=1
# 		pf.close()
# 		##get txt count
# 		txtfn=file_id+'.txt'
# 		txtf=open(txtdir+txtfn, 'rU')
# 		txtlines=txtf.readlines()
# 		filter(None, txtlines)
# 		txtcount=len(txtlines)
# 		##get lemmaxml count
# 		#<sentence id="1">
# 		lxfn=file_id+'.xml'
# 		lxf=open(lemmaxmldir+lxfn, 'rU')
# 		lxlines=lxf.readlines()
# 		lxcount=0
# 		for lxline in lxlines:
# 			if lxline.strip()=='''<sentence id="1">''':
# 				lxcount+=1
# 			else: pass
# 		##check for matching counts; order here copies the order the files are produced via the shell: csvcount, txtcount, lxcount, pcount, lkcount, lccount
# 		integercounts={'csvcount':csvcount, 'txtcount':txtcount, 'lxcount':lxcount, 'pcount':pcount, 'lkcount':lkcount, 'lccount':lccount}
# 		orderlist=['csvcount', 'txtcount', 'lxcount', 'pcount', 'lkcount', 'lccount']
# 		stringdict={}
# 		for o in orderlist:
# 			stringdict[o]=str(integercounts[o])
# 		if stringdict['csvcount']==stringdict['txtcount']==stringdict['lxcount']==stringdict['pcount']==stringdict['lkcount']==stringdict['lccount']:
# 			matching.append([file_id, stringdict['csvcount'], stringdict['txtcount'], stringdict['lxcount'], stringdict['pcount'], stringdict['lkcount'], stringdict['lccount']])
# 		else:
# 			nonmatching.append([file_id, stringdict['csvcount'], stringdict['txtcount'], stringdict['lxcount'], stringdict['pcount'], stringdict['lkcount'], stringdict['lccount']])
# 		#print file_id+'\t'+str(csvcount)+'\t'+str(lccount)+'\n'
# 	print 'Non-Matches:'
# 	for nm in nonmatching:
# 		print '\t'.join(nm)
# 		
# 	print '\nMatches:'
# 	for m in matching:
# 		print '\t'.join(m)
# 	return nonmatching
# 
# def show_responses(nm): ## i want this function to go through the non-matching cases and show response by response, the txt and lemma_conll, so I can find where the mismatch begins.
# 	for n in nm:
# 		file_id=n[0]
# 		print '\n'+file_id
# 		txtfn=file_id+'.txt'
# 		txtf=open(txtdir+txtfn, 'rU')
# 		txtsents=txtf.readlines()
# 		filter(None, txtsents)
# 		lcfn=file_id+'.lemma_conll'
# 		lcf=open(lcdir+lcfn, 'rU')
# 		lcfull=lcf.read()
# 		#print lcfull
# 		lcsents=lcfull.split('\n\n')
# 		filter(None, lcsents)
# 		#print lcsents
# 		count=1
# 		while txtsents or lcsents:
# 			try:
# 				t=txtsents.pop(0)
# 			except:
# 				t='EMPTY (txt)'
# 			try:
# 				lcurrent=lcsents.pop(0)
# 				lcurrent=lcurrent.split('\n')
# 			except:
# 				l='No LC to pop'
# 			try:
# 				ls=[]
# 				for row in lcurrent:
# 					#print row
# 					word=row.split('\t')[1]
# 					#print word
# 					ls.append(word)
# 					l=' '.join(ls)
# 			except:
# 				l='EMPTY (lemma_conll)'
# 			print str(count)+'\t'+t.strip()+'\n'+str(count)+'\t'+l.strip()+'\n'
# 			count+=1
# 		print '\n\n'


#check_file_lengths()
myfiles=get_all_lemma_conll_filenames()
hs=get_handles(myfiles)
for hx in hs:
	pd=get_parse_dict(hx)
	fill_csvs_with_parse(hx, pd)
	#for k in pd:
		#print k
		#print pd[k]
	#fill_lc_with_parse(hx, pd)

#print hs
#print len(hs)
# 
# all_ns=[]
# for myf in myfiles:
# 	if "all_ns" in myf:
# 		all_ns.append(myf)
# 	else: pass
# all_ns.sort()
# nonmatching=check_file_lengths(all_ns)
# show_responses(nonmatching)