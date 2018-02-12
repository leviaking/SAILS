#!/usr/bin/env python

import sys, csv, itertools, os
from shutil import copyfile

##This is probably the ugliest script I've ever written, but I only need it once, so fast and dirty it is!

def transform_response(myresp):
	tresp=' '.join(myresp.split())
	tresp=tresp.strip(' .!')
	tresp=tresp.lower()
	return tresp

for n in range(1,31):
	nstr=str(n).zfill(2)
	masterTfilename='masters/I'+nstr+'T_master_no_anno.csv'
	masterUfilename='masters/I'+nstr+'T_master_no_anno.csv'
	masterToutname='masters/I'+nstr+'T_master_anno.csv'
	masterUoutname='masters/I'+nstr+'U_master_anno.csv'

	masterTfile=open(masterTfilename, 'r')
	masterUfile=open(masterUfilename, 'r')
	masterTreader=csv.reader(masterTfile, dialect=csv.excel)
	masterUreader=csv.reader(masterUfile, dialect=csv.excel)
	masterTheader=next(masterTreader, None)
	masterUheader=next(masterUreader, None)
	masterTheader=masterTheader+['A1 Core', 'A1 Answer', 'A1 Gramm', 'A1 Interp', 'A1 Verif', 'A2 Core', 'A2 Answer', 'A2 Gramm', 'A2 Interp', 'A2 Verif']
	masterUheader=masterUheader+['A1 Core', 'A1 Answer', 'A1 Gramm', 'A1 Interp', 'A1 Verif', 'A2 Core', 'A2 Answer', 'A2 Gramm', 'A2 Interp', 'A2 Verif']
	masterToutrows=[masterTheader]
	masterUoutrows=[masterUheader]
	
	A1coreTfilename='Core/A1seconpassanno_I'+nstr+'T_Core.csv'
	A1coreUfilename='Core/A1secondpassanno_I'+nstr+'U_Core.csv'
	A1coreTfile=open(A1coreTfilename, 'r')
	A1coreUfile=open(A1coreUfilename, 'r')
	A1coreTreader=csv.reader(A1coreTfile, dialect=csv.excel)
	A1coreUreader=csv.reader(A1coreUfile, dialect=csv.excel)
	skipheader=next(A1coreTreader, None)
	skipheader=next(A1coreUreader, None)
	A1coreTanno={}
	A1coreUanno={}
	for row in A1coreTreader:
		A1coreTanno[row[0].strip()]=row[1]
	for row in A1coreUreader:
		A1coreUanno[row[0].strip()]=row[1]
	A1coreTfile.close()
	A1coreUfile.close()

	A1answerTfilename='Answer/A1seconpassanno_I'+nstr+'T_Answer.csv'
	A1answerUfilename='Answer/A1secondpassanno_I'+nstr+'U_Answer.csv'
	A1answerTfile=open(A1answerTfilename, 'r')
	A1answerUfile=open(A1answerUfilename, 'r')
	A1answerTreader=csv.reader(A1answerTfile, dialect=csv.excel)
	A1answerUreader=csv.reader(A1answerUfile, dialect=csv.excel)
	skipheader=next(A1answerTreader, None)
	skipheader=next(A1answerUreader, None)
	A1answerTanno={}
	A1answerUanno={}
	for row in A1answerTreader:
		A1answerTanno[row[0].strip()]=row[1]
	for row in A1answerUreader:
		A1answerUanno[row[0].strip()]=row[1]
	A1answerTfile.close()
	A1answerUfile.close()
	
	A1grammTfilename='Gramm/A1seconpassanno_I'+nstr+'T_Gramm.csv'
	A1grammUfilename='Gramm/A1secondpassanno_I'+nstr+'U_Gramm.csv'
	A1grammTfile=open(A1grammTfilename, 'r')
	A1grammUfile=open(A1grammUfilename, 'r')
	A1grammTreader=csv.reader(A1grammTfile, dialect=csv.excel)
	A1grammUreader=csv.reader(A1grammUfile, dialect=csv.excel)
	skipheader=next(A1grammTreader, None)
	skipheader=next(A1grammUreader, None)
	A1grammTanno={}
	A1grammUanno={}
	for row in A1grammTreader:
		A1grammTanno[row[0].strip()]=row[1]
	for row in A1grammUreader:
		A1grammUanno[row[0].strip()]=row[1]
	A1grammTfile.close()
	A1grammUfile.close()
	
	A1interpTfilename='Interp/A1seconpassanno_I'+nstr+'T_Interp.csv'
	A1interpUfilename='Interp/A1secondpassanno_I'+nstr+'U_Interp.csv'
	A1interpTfile=open(A1interpTfilename, 'r')
	A1interpUfile=open(A1interpUfilename, 'r')
	A1interpTreader=csv.reader(A1interpTfile, dialect=csv.excel)
	A1interpUreader=csv.reader(A1interpUfile, dialect=csv.excel)
	skipheader=next(A1interpTreader, None)
	skipheader=next(A1interpUreader, None)
	A1interpTanno={}
	A1interpUanno={}
	for row in A1interpTreader:
		A1interpTanno[row[0].strip()]=row[1]
	for row in A1interpUreader:
		A1interpUanno[row[0].strip()]=row[1]
	A1interpTfile.close()
	A1interpUfile.close()
	
	A1verifTfilename='Verif/A1seconpassanno_I'+nstr+'T_Verif.csv'
	A1verifUfilename='Verif/A1secondpassanno_I'+nstr+'U_Verif.csv'
	A1verifTfile=open(A1verifTfilename, 'r')
	A1verifUfile=open(A1verifUfilename, 'r')
	A1verifTreader=csv.reader(A1verifTfile, dialect=csv.excel)
	A1verifUreader=csv.reader(A1verifUfile, dialect=csv.excel)
	skipheader=next(A1verifTreader, None)
	skipheader=next(A1verifUreader, None)
	A1verifTanno={}
	A1verifUanno={}
	for row in A1verifTreader:
		A1verifTanno[row[0].strip()]=row[1]
	for row in A1verifUreader:
		A1verifUanno[row[0].strip()]=row[1]
	A1verifTfile.close()
	A1verifUfile.close()
		
	for mTrow in masterTreader:
		mTresp=mTrow[12]
		outTrow=list(mTresp)
		mrTt=transform_response(mTresp)
		if mrTt in A1coreTanno:
			outTrow=outTrow+[A1coreTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if mrTt in A1answerTanno:
			outTrow=outTrow+[A1answerTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if mrTt in A1grammTanno:
			outTrow=outTrow+[A1grammTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if mrTt in A1interpTanno:
			outTrow=outTrow+[A1interpTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if mrTt in A1verifTanno:
			outTrow=outTrow+[A1verifTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		masterToutrows.append(outTrow)
	masterTfile.close()

	for mUrow in masterUreader:
		mUresp=mUrow[12]
		outUrow=list(mUresp)
		mrUt=transform_response(mUresp)
		if mrUt in A1coreUanno:
			outUrow=outUrow+[A1coreUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if mrUt in A1answerUanno:
			outUrow=outUrow+[A1answerUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if mrUt in A1grammUanno:
			outUrow=outUrow+[A1grammUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if mrUt in A1interpUanno:
			outUrow=outUrow+[A1interpUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if mrUt in A1verifUanno:
			outUrow=outUrow+[A1verifUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		masterUoutrows.append(outUrow)
	masterUfile.close()
	
	
	masterTout=open(masterToutname, 'w')
	masterUout=open(masterUoutname, 'w')
	Twriter=csv.writer(masterTout, dialect=csv.excel)
	Uwriter=csv.writer(masterUout, dialect=csv.excel)
	
	for Tr in masterToutrows:
		Twriter.writerow(Tr)
	for Ur in masterUoutrows:
		Uwriter.writerow(Ur)
	
	masterTout.close()
	masterUout.close()
