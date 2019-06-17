#!/usr/bin/env python

##This script takes the annotation files and outputs a single csv with many different agreement measures. This includes agreement scores per item per feature, but also averages per item, and per feature, and for targeted/untargeted.


import sys, re, csv, datetime, os, random
from shutil import copyfile

def float_sum(floatlist):
    mysum = 0
    for i in floatlist:
        mysum = mysum + i
    return mysum

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

tuversions = ['T', 'U']

allrids=[] ##rid = RID = Respondent ID
allhandlecounts={}

outheader=	['NSv1 participants', 'NSv2 participants', 'NSv1pt1 participants', 'NSv1pt2 participants', 'NSv2pt1 participants', 'NSv2pt2 participants', 'NNSv1 participants', 'NNSv2 participants', 'NSv1', 'NSv2', 'NSv1pt1', 'NSv1pt2', 'NSv2pt1', 'NSv2pt2', 'NNSv1', 'NNSv2']

def gen_handles():
	handles=[]
	for num in range(1, 31):
		numstr=str(num).zfill(2)
		for tu in tuversions:
			handle=''.join(['I',numstr,tu])
			handles.append(handle)
	return handles
	
def get_row_info(myrow):
	if str(myrow[12]).strip()=='0':
		return 'NA', 'NA'	
	else:
		myrowrid = str(myrow[0]).strip()
		myrowsource=str(myrow[2]).strip()
		return myrowrid, myrowsource

def get_handle_counts(handle): ##we'll use this to process a single file (item number + targeted or untargeted)
	handle_counts={'NSv1':0, 'NSv2':0, 'NSv1pt1':0, 'NSv1pt2':0, 'NSv2pt1':0, 'NSv2pt2':0, 'NNSv1':0, 'NNSv2':0}
	infilename=''.join([handle,'_master_anno.csv'])
	infile=open(infilename, 'rU')
	infreader=csv.reader(infile, dialect=csv.excel)
	skipheader=next(infreader, None)
	handlerids=[]
	for row in infreader:
		rowrid, rowsource = get_row_info(row)
		if rowrid=='NA':
			pass
		else:
			if rowrid not in handlerids:
				handlerids.append(rowrid)
			else: pass
			handle_counts[rowsource]+=1
	infile.close()
	for rowrid in handlerids:
		if rowrid not in allrids:
			allrids.append(rowrid)
	allhandlecounts[handle]=handle_counts
	


allhandles=gen_handles()
for h in allhandles:
	get_handle_counts(h)

for h in allhandles:
	print h, allhandlecounts[h]
# 
# 
# for speaker in speakers:
# 	for num in range(1,31):
# 		numstr=str(num).zfill(2)
# 		for tu in tuversions:
# 			myhandle=speaker+'_'+numstr+'_'+tu
# 			myfilename=myhandle+'_responses.csv'
# 			myfile=open(myfilename, 'rU')
# 			myfreader=csv.reader(myfile, dialect=csv.excel)
# 			myfrows=[]
# 			for mz in myfreader:
# 				m=mz[0]
# 				myfrows.append(m.strip())
# 			myfile.close()
# 			allhandles.append(myhandle)
# 			handledict[myhandle]=myfrows
# 
# for speaker in speakers:
# 	for num in range(1,31):
# 		numstr=str(num).zfill(2)
# 		for tu in tuversions:
# 			current_ratios=[]
# 			counter=0
# 			mh=speaker+'_'+numstr+'_'+tu
# 			myresponses=handledict[mh]
# 			while counter < iterations:
# 				mytypes=[]
# 				mytokens=random.sample(myresponses, samplesize)
# 				for mytoken in mytokens:
# 					mt=transform_response(mytoken)
# 					if mt in mytypes:
# 						pass
# 					else:
# 						mytypes.append(mt)
# 				myttr=float(len(mytypes))/float(len(mytokens))
# 				current_ratios.append(myttr)
# 				counter+=1
# 			cr=float(float_sum(current_ratios))/float(len(current_ratios))
# 			if numstr in intrans:
# 				if speaker=='L1':
# 					if tu=='T':
# 						l1_intrans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l1_intrans_u_ratios.append(cr)
# 					else:
# 						pass
# 				elif speaker=='L2':
# 					if tu=='T':
# 						l2_intrans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l2_intrans_u_ratios.append(cr)
# 					else:
# 						pass
# 				else:
# 					pass
# 			elif numstr in trans:
# 				if speaker=='L1':
# 					if tu=='T':
# 						l1_trans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l1_trans_u_ratios.append(cr)
# 					else:
# 						pass
# 				elif speaker=='L2':
# 					if tu=='T':
# 						l2_trans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l2_trans_u_ratios.append(cr)
# 					else:
# 						pass
# 				else:
# 					pass
# 			elif numstr in ditrans:
# 				if speaker=='L1':
# 					if tu=='T':
# 						l1_ditrans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l1_ditrans_u_ratios.append(cr)
# 					else:
# 						pass
# 				elif speaker=='L2':
# 					if tu=='T':
# 						l2_ditrans_t_ratios.append(cr)
# 					elif tu=='U':
# 						l2_ditrans_u_ratios.append(cr)
# 					else:
# 						pass
# 				else:
# 					pass				
# 			else:
# 				pass
# 
# translist=['l1_intrans_t', 'l1_trans_t', 'l1_ditrans_t', 'l2_intrans_t', 'l2_trans_t', 'l2_ditrans_t', 'l1_intrans_u', 'l1_trans_u', 'l1_ditrans_u', 'l2_intrans_u', 'l2_trans_u', 'l2_ditrans_u']
# ratios_dict={'l1_intrans_t': l1_intrans_t_ratios, 'l1_trans_t': l1_trans_t_ratios, 'l1_ditrans_t': l1_ditrans_t_ratios, 'l2_intrans_t': l2_intrans_t_ratios, 'l2_trans_t': l2_trans_t_ratios, 'l2_ditrans_t': l2_ditrans_t_ratios, 'l1_intrans_u': l1_intrans_u_ratios, 'l1_trans_u': l1_trans_u_ratios, 'l1_ditrans_u': l1_ditrans_u_ratios, 'l2_intrans_u': l2_intrans_u_ratios, 'l2_trans_u': l2_trans_u_ratios, 'l2_ditrans_u': l2_ditrans_u_ratios}
# 
# # for r in translist:
# # 	print r
# # 	rl = ratios_dict[r]
# # 	ttr=float(float_sum(rl))/float(len(rl))
# # 	print ttr
# # 	print '\n'

