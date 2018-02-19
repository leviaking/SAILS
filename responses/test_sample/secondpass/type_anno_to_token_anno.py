#!/usr/bin/env python

import sys, csv, itertools, os
from shutil import copyfile

##This is probably the ugliest script I've ever written, but I only need it once, so fast and dirty it is! This applies the annotations from the response type files to the response tokens and writes a new file.

A2annoitems=[28,29,30]

def transform_response(myresp):
	tresp=' '.join(myresp.split())
	tresp=tresp.strip(' .!')
	tresp=tresp.lower()
	return tresp

for n in range(28,31):
	nstr=str(n).zfill(2)
	masterTfilename='masters/I'+nstr+'T_master_no_anno.csv'
	#print masterTfilename
	masterUfilename='masters/I'+nstr+'U_master_no_anno.csv'
	#print masterUfilename
	masterToutname='masters/I'+nstr+'T_master_anno.csv'
	masterUoutname='masters/I'+nstr+'U_master_anno.csv'

	masterTfile=open(masterTfilename, 'rU')
	masterUfile=open(masterUfilename, 'rU')
	masterTreader=csv.reader(masterTfile, dialect=csv.excel)
	masterUreader=csv.reader(masterUfile, dialect=csv.excel)
	masterTheader=next(masterTreader, None)
	masterUheader=next(masterUreader, None)
	masterTheader=masterTheader+['A1 Core', 'A1 Answer', 'A1 Gramm', 'A1 Interp', 'A1 Verif', 'A2 Core', 'A2 Answer', 'A2 Gramm', 'A2 Interp', 'A2 Verif']
	masterUheader=masterUheader+['A1 Core', 'A1 Answer', 'A1 Gramm', 'A1 Interp', 'A1 Verif', 'A2 Core', 'A2 Answer', 'A2 Gramm', 'A2 Interp', 'A2 Verif']
	masterToutrows=[masterTheader]
	masterUoutrows=[masterUheader]
	
	A1coreTfilename='Core/A1secondpassanno_I'+nstr+'T_Core.csv'
	#print A1coreTfilename
	A1coreUfilename='Core/A1secondpassanno_I'+nstr+'U_Core.csv'
	#print A1coreUfilename
	A1coreTfile=open(A1coreTfilename, 'rU')
	A1coreUfile=open(A1coreUfilename, 'rU')
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

	A1answerTfilename='Answer/A1secondpassanno_I'+nstr+'T_Answer.csv'
	#print A1answerTfilename
	A1answerUfilename='Answer/A1secondpassanno_I'+nstr+'U_Answer.csv'
	#print A1answerUfilename
	A1answerTfile=open(A1answerTfilename, 'rU')
	A1answerUfile=open(A1answerUfilename, 'rU')
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
	
	A1grammTfilename='Gramm/A1secondpassanno_I'+nstr+'T_Gramm.csv'
	#print A1grammTfilename
	A1grammUfilename='Gramm/A1secondpassanno_I'+nstr+'U_Gramm.csv'
	#print A1grammUfilename
	A1grammTfile=open(A1grammTfilename, 'rU')
	A1grammUfile=open(A1grammUfilename, 'rU')
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
	
	A1interpTfilename='Interp/A1secondpassanno_I'+nstr+'T_Interp.csv'
	#print A1interpTfilename
	A1interpUfilename='Interp/A1secondpassanno_I'+nstr+'U_Interp.csv'
	# print A1interpUfilename
	A1interpTfile=open(A1interpTfilename, 'rU')
	A1interpUfile=open(A1interpUfilename, 'rU')
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
	
	A1verifTfilename='Verif/A1secondpassanno_I'+nstr+'T_Verif.csv'
	# print A1verifTfilename
	A1verifUfilename='Verif/A1secondpassanno_I'+nstr+'U_Verif.csv'
	# print A1verifUfilename
	A1verifTfile=open(A1verifTfilename, 'rU')
	A1verifUfile=open(A1verifUfilename, 'rU')
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

	if n in A2annoitems:	
		A2coreTfilename='Core/A2secondpassanno_I'+nstr+'T_Core.csv'
		# print A2coreTfilename
		A2coreUfilename='Core/A2secondpassanno_I'+nstr+'U_Core.csv'
		# print A2coreUfilename
		A2coreTfile=open(A2coreTfilename, 'rU')
		A2coreUfile=open(A2coreUfilename, 'rU')
		A2coreTreader=csv.reader(A2coreTfile, dialect=csv.excel)
		A2coreUreader=csv.reader(A2coreUfile, dialect=csv.excel)
		skipheader=next(A2coreTreader, None)
		skipheader=next(A2coreUreader, None)
		A2coreTanno={}
		A2coreUanno={}
		for row in A2coreTreader:
			A2coreTanno[row[0].strip()]=row[1]
		for row in A2coreUreader:
			A2coreUanno[row[0].strip()]=row[1]
		A2coreTfile.close()
		A2coreUfile.close()
	
		A2answerTfilename='Answer/A2secondpassanno_I'+nstr+'T_Answer.csv'
		# print A2answerTfilename
		A2answerUfilename='Answer/A2secondpassanno_I'+nstr+'U_Answer.csv'
		# print A2answerUfilename
		A2answerTfile=open(A2answerTfilename, 'rU')
		A2answerUfile=open(A2answerUfilename, 'rU')
		A2answerTreader=csv.reader(A2answerTfile, dialect=csv.excel)
		A2answerUreader=csv.reader(A2answerUfile, dialect=csv.excel)
		skipheader=next(A2answerTreader, None)
		skipheader=next(A2answerUreader, None)
		A2answerTanno={}
		A2answerUanno={}
		for row in A2answerTreader:
			A2answerTanno[row[0].strip()]=row[1]
		for row in A2answerUreader:
			A2answerUanno[row[0].strip()]=row[1]
		A2answerTfile.close()
		A2answerUfile.close()
		
		A2grammTfilename='Gramm/A2secondpassanno_I'+nstr+'T_Gramm.csv'
		# print A2grammTfilename
		A2grammUfilename='Gramm/A2secondpassanno_I'+nstr+'U_Gramm.csv'
		# print A2grammTfilename
		A2grammTfile=open(A2grammTfilename, 'rU')
		A2grammUfile=open(A2grammUfilename, 'rU')
		A2grammTreader=csv.reader(A2grammTfile, dialect=csv.excel)
		A2grammUreader=csv.reader(A2grammUfile, dialect=csv.excel)
		skipheader=next(A2grammTreader, None)
		skipheader=next(A2grammUreader, None)
		A2grammTanno={}
		A2grammUanno={}
		for row in A2grammTreader:
			A2grammTanno[row[0].strip()]=row[1]
		for row in A2grammUreader:
			A2grammUanno[row[0].strip()]=row[1]
		A2grammTfile.close()
		A2grammUfile.close()
		
		A2interpTfilename='Interp/A2secondpassanno_I'+nstr+'T_Interp.csv'
		# print A2interpTfilename
		A2interpUfilename='Interp/A2secondpassanno_I'+nstr+'U_Interp.csv'
		# print A2interpUfilename
		A2interpTfile=open(A2interpTfilename, 'rU')
		A2interpUfile=open(A2interpUfilename, 'rU')
		A2interpTreader=csv.reader(A2interpTfile, dialect=csv.excel)
		A2interpUreader=csv.reader(A2interpUfile, dialect=csv.excel)
		skipheader=next(A2interpTreader, None)
		skipheader=next(A2interpUreader, None)
		A2interpTanno={}
		A2interpUanno={}
		for row in A2interpTreader:
			A2interpTanno[row[0].strip()]=row[1]
		for row in A2interpUreader:
			A2interpUanno[row[0].strip()]=row[1]
		A2interpTfile.close()
		A2interpUfile.close()
		
		A2verifTfilename='Verif/A2secondpassanno_I'+nstr+'T_Verif.csv'
		# print A2verifTfilename
		A2verifUfilename='Verif/A2secondpassanno_I'+nstr+'U_Verif.csv'
		# print A2verifUfilename
		A2verifTfile=open(A2verifTfilename, 'rU')
		A2verifUfile=open(A2verifUfilename, 'rU')
		A2verifTreader=csv.reader(A2verifTfile, dialect=csv.excel)
		A2verifUreader=csv.reader(A2verifUfile, dialect=csv.excel)
		skipheader=next(A2verifTreader, None)
		skipheader=next(A2verifUreader, None)
		A2verifTanno={}
		A2verifUanno={}
		for row in A2verifTreader:
			A2verifTanno[row[0].strip()]=row[1]
		for row in A2verifUreader:
			A2verifUanno[row[0].strip()]=row[1]
		A2verifTfile.close()
		A2verifUfile.close()
			

	for mTrow in masterTreader:
		mTresp=mTrow[12]
		outTrow=list(mTrow)
		outTtail=[]
		mrTt=transform_response(mTresp)
		if mrTt in A1coreTanno:
			outTrow=outTrow+[A1coreTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if n in A2annoitems:
			if mrTt in A2coreTanno:
				outTtail=outTtail+[A2coreTanno[mrTt]]
			else:
				pass
		else:
			pass
		if mrTt in A1answerTanno:
			outTrow=outTrow+[A1answerTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if n in A2annoitems:
			if mrTt in A2answerTanno:
				outTtail=outTtail+[A2answerTanno[mrTt]]
			else:
				pass
		else:
			pass
		if mrTt in A1grammTanno:
			outTrow=outTrow+[A1grammTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if n in A2annoitems:
			if mrTt in A2grammTanno:
				outTtail=outTtail+[A2grammTanno[mrTt]]
			else:
				pass
		else:
			pass
		if mrTt in A1interpTanno:
			outTrow=outTrow+[A1interpTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if n in A2annoitems:
			if mrTt in A2interpTanno:
				outTtail=outTtail+[A2interpTanno[mrTt]]
			else:
				pass
		else:
			pass
		if mrTt in A1verifTanno:
			outTrow=outTrow+[A1verifTanno[mrTt]]
		else:
			outTrow=outTrow+[' ']
		if n in A2annoitems:
			if mrTt in A2verifTanno:
				outTtail=outTtail+[A2verifTanno[mrTt]]
			else:
				pass
		else:
			pass
		outTrow=outTrow+outTtail
		masterToutrows.append(outTrow)

	for mUrow in masterUreader:
		mUresp=mUrow[12]
		outUrow=list(mUrow)
		outUtail=[]
		mrUt=transform_response(mUresp)
		if mrUt in A1coreUanno:
			outUrow=outUrow+[A1coreUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if n in A2annoitems:
			if mrUt in A2coreUanno:
				outUtail=outUtail+[A2coreUanno[mrUt]]
			else:
				pass
		else:
			pass
		if mrUt in A1answerUanno:
			outUrow=outUrow+[A1answerUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if n in A2annoitems:
			if mrUt in A2answerUanno:
				outUtail=outUtail+[A2answerUanno[mrUt]]
			else:
				pass
		else:
			pass
		if mrUt in A1grammUanno:
			outUrow=outUrow+[A1grammUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if n in A2annoitems:
			if mrUt in A2grammUanno:
				outUtail=outUtail+[A2grammUanno[mrUt]]
			else:
				pass
		else:
			pass
		if mrUt in A1interpUanno:
			outUrow=outUrow+[A1interpUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if n in A2annoitems:
			if mrUt in A2interpUanno:
				outUtail=outUtail+[A2interpUanno[mrUt]]
			else:
				pass
		else:
			pass
		if mrUt in A1verifUanno:
			outUrow=outUrow+[A1verifUanno[mrUt]]
		else:
			outUrow=outUrow+[' ']
		if n in A2annoitems:
			if mrUt in A2verifUanno:
				outUtail=outUtail+[A2verifUanno[mrUt]]
			else:
				pass
		else:
			pass
		outUrow=outUrow+outUtail
		masterUoutrows.append(outUrow)


	masterUfile.close()
	masterTfile.close()


	masterTout=open(masterToutname, 'w')
	masterUout=open(masterUoutname, 'w')
	Twriter=csv.writer(masterTout, dialect=csv.excel)
	Uwriter=csv.writer(masterUout, dialect=csv.excel)
	
	for tr in masterToutrows:
		Twriter.writerow(tr)
	for ur in masterUoutrows:
		Uwriter.writerow(ur)
	
	masterTout.close()
	masterUout.close()
