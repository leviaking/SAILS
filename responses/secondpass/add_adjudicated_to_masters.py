#!/usr/bin/env python

import sys, csv, itertools, os
from shutil import copyfile

##This is adapted from "type_anno_to_token_anno.py". One of the ugliest scripts I've ever written, but I only need it once, so fast and dirty it is!
##This takes the individual item token masters, which already contain the five layers of annotation from both A1 and A2. Responses with disagreements were re-examined and re-annotated by each A1 and A2, together. Some disagreements are reconciled, but some are not. This script adds these new annotations to a copy of the master files. 

A2annoitems=[1,2,3]

def transform_response(myresp):
	tresp=' '.join(myresp.split())
	tresp=tresp.strip(' .!')
	tresp=tresp.lower()
	return tresp

for n in range(1,4):
	nstr=str(n).zfill(2)
	masterTfilename='masters/I'+nstr+'T_master_anno.csv'
	#print masterTfilename
	masterUfilename='masters/I'+nstr+'U_master_anno.csv'
	#print masterUfilename
	masterToutname='masters/I'+nstr+'T_master_adjudicated.csv'
	masterUoutname='masters/I'+nstr+'U_master_adjudicated.csv'

	masterTfile=open(masterTfilename, 'rU')
	masterUfile=open(masterUfilename, 'rU')
	masterTreader=csv.reader(masterTfile, dialect=csv.excel)
	masterUreader=csv.reader(masterUfile, dialect=csv.excel)
	masterTheader=next(masterTreader, None)
	masterUheader=next(masterUreader, None)
	##both headers are: ['A1 Core', 'A1 Answer', 'A1 Gramm', 'A1 Interp', 'A1 Verif', 'A2 Core', 'A2 Answer', 'A2 Gramm', 'A2 Interp', 'A2 Verif']
	masterTheader=masterTheader+['A1b Core', 'A1b Answer', 'A1b Gramm', 'A1b Interp', 'A1b Verif', 'A2b Core', 'A2b Answer', 'A2b Gramm', 'A2b Interp', 'A2b Verif']
	masterUheader=masterUheader+['A1b Core', 'A1b Answer', 'A1b Gramm', 'A1b Interp', 'A1b Verif', 'A2b Core', 'A2b Answer', 'A2b Gramm', 'A2b Interp', 'A2b Verif']
	masterToutrows=[masterTheader]
	masterUoutrows=[masterUheader]
	mTrows=[]
	mUrows=[]
	for row in masterTreader:
		mTrows.append(row)
	for row in masterUreader:
		mUrows.append(row)
	masterTfile.close()
	masterUfile.close()
	
	coreTname='adjudicated/I'+nstr+'T_Core_type_adjudicated.csv'
	print coreTname
	coreUname='adjudicated/I'+nstr+'U_Core_type_adjudicated.csv'
	print coreUname
	coreT=open(coreTname, 'rU')
	coreU=open(coreUname, 'rU')
	coreTreader=csv.reader(coreT, dialect=csv.excel)
	coreUreader=csv.reader(coreU, dialect=csv.excel)
	skipheader=next(coreTreader, None)
	skipheader=next(coreTreader, None)
	coreTdict={}
	coreUdict={}
	for Tr in coreTreader:
		coreTdict[Tr[1].strip()]=Tr[2:6]
	for Ur in coreUreader:
		coreUdict[Ur[1].strip()]=Ur[2:6]
	coreT.close()
	coreU.close()

	answerTname='adjudicated/I'+nstr+'T_Answer_type_adjudicated.csv'
	answerUname='adjudicated/I'+nstr+'U_Answer_type_adjudicated.csv'
	answerT=open(answerTname, 'rU')
	answerU=open(answerUname, 'rU')
	answerTreader=csv.reader(answerT, dialect=csv.excel)
	answerUreader=csv.reader(answerU, dialect=csv.excel)
	skipheader=next(answerTreader, None)
	skipheader=next(answerTreader, None)
	answerTdict={}
	answerUdict={}
	for Tr in answerTreader:
		answerTdict[Tr[1].strip()]=Tr[2:6]
	for Ur in answerUreader:
		answerUdict[Ur[1].strip()]=Ur[2:6]
	answerT.close()
	answerU.close()

	grammTname='adjudicated/I'+nstr+'T_Gramm_type_adjudicated.csv'
	grammUname='adjudicated/I'+nstr+'U_Gramm_type_adjudicated.csv'
	grammT=open(grammTname, 'rU')
	grammU=open(grammUname, 'rU')
	grammTreader=csv.reader(grammT, dialect=csv.excel)
	grammUreader=csv.reader(grammU, dialect=csv.excel)
	skipheader=next(grammTreader, None)
	skipheader=next(grammTreader, None)
	grammTdict={}
	grammUdict={}
	for Tr in grammTreader:
		grammTdict[Tr[1].strip()]=Tr[2:6]
	for Ur in grammUreader:
		grammUdict[Ur[1].strip()]=Ur[2:6]
	grammT.close()
	grammU.close()
	
	interpTname='adjudicated/I'+nstr+'T_Interp_type_adjudicated.csv'
	interpUname='adjudicated/I'+nstr+'U_Interp_type_adjudicated.csv'
	interpT=open(interpTname, 'rU')
	interpU=open(interpUname, 'rU')
	interpTreader=csv.reader(interpT, dialect=csv.excel)
	interpUreader=csv.reader(interpU, dialect=csv.excel)
	skipheader=next(interpTreader, None)
	skipheader=next(interpTreader, None)
	interpTdict={}
	interpUdict={}
	for Tr in interpTreader:
		interpTdict[Tr[1].strip()]=Tr[2:6]
	for Ur in interpUreader:
		interpUdict[Ur[1].strip()]=Ur[2:6]
	interpT.close()
	interpU.close()
	
	verifTname='adjudicated/I'+nstr+'T_Verif_type_adjudicated.csv'
	verifUname='adjudicated/I'+nstr+'U_Verif_type_adjudicated.csv'
	verifT=open(verifTname, 'rU')
	verifU=open(verifUname, 'rU')
	verifTreader=csv.reader(verifT, dialect=csv.excel)
	verifUreader=csv.reader(verifU, dialect=csv.excel)
	skipheader=next(verifTreader, None)
	skipheader=next(verifTreader, None)
	verifTdict={}
	verifUdict={}
	for Tr in verifTreader:
		verifTdict[Tr[1].strip()]=Tr[2:6]
	for Ur in verifUreader:
		verifUdict[Ur[1].strip()]=Ur[2:6]
	verifT.close()
	verifU.close()

	for rowT in mTrows:
		respT = rowT[12]
		if respT == '0':
			masterToutrows.append(rowT)
		else:
			trespT = transform_response(respT)
			if trespT in coreTdict:
				A1bTCore=coreTdict[trespT][2]
				A2bTCore=coreTdict[trespT][3]
			else:
				A1bTCore=rowT[13]
				A2bTCore=rowT[18]
			if trespT in answerTdict:
				A1bTAnswer=answerTdict[trespT][2]
				A2bTAnswer=answerTdict[trespT][3]
			else:
				A1bTAnswer=rowT[14]
				A2bTAnswer=rowT[19]
			if trespT in grammTdict:
				A1bTGramm=grammTdict[trespT][2]
				A2bTGramm=grammTdict[trespT][3]
			else:
				A1bTGramm=rowT[15]
				A2bTGramm=rowT[20]
			if trespT in interpTdict:
				# print trespT
				# print interpTdict[trespT]
				A1bTInterp=interpTdict[trespT][2]
				A2bTInterp=interpTdict[trespT][3]
			else:
				A1bTInterp=rowT[16]
				A2bTInterp=rowT[21]
			if trespT in verifTdict:
				A1bTVerif=verifTdict[trespT][2]
				A2bTVerif=verifTdict[trespT][3]
			else:
				A1bTVerif=rowT[17]
				A2bTVerif=rowT[22]
			Tmorow=rowT+[A1bTCore, A1bTAnswer, A1bTGramm, A1bTInterp, A1bTVerif, A2bTCore, A2bTAnswer, A2bTGramm, A2bTInterp, A2bTVerif]
			masterToutrows.append(Tmorow)
			
	for rowU in mUrows:
		respU = rowU[12]
		if respU == '0':
			masterUoutrows.append(rowU)
		else:
			trespU = transform_response(respU)
			if trespU in coreUdict:
				A1bUCore=coreUdict[trespU][2]
				A2bUCore=coreUdict[trespU][3]
			else:
				A1bUCore=rowU[13]
				A2bUCore=rowU[18]
			if trespU in answerUdict:
				A1bUAnswer=answerUdict[trespU][2]
				A2bUAnswer=answerUdict[trespU][3]
			else:
				A1bUAnswer=rowU[14]
				A2bUAnswer=rowU[19]
			if trespU in grammUdict:
				A1bUGramm=grammUdict[trespU][2]
				A2bUGramm=grammUdict[trespU][3]
			else:
				A1bUGramm=rowU[15]
				A2bUGramm=rowU[20]
			if trespU in interpUdict:
				A1bUInterp=interpUdict[trespU][2]
				A2bUInterp=interpUdict[trespU][3]
			else:
				A1bUInterp=rowU[16]
				A2bUInterp=rowU[21]
			if trespU in verifUdict:
				A1bUVerif=verifUdict[trespU][2]
				A2bUVerif=verifUdict[trespU][3]
			else:
				A1bUVerif=rowU[17]
				A2bUVerif=rowU[22]
			Umorow=rowU+[A1bUCore, A1bUAnswer, A1bUGramm, A1bUInterp, A1bUVerif, A2bUCore, A2bUAnswer, A2bUGramm, A2bUInterp, A2bUVerif]
			masterUoutrows.append(Umorow)
			
	TR=open(masterToutname, 'w')
	TRwriter=csv.writer(TR, dialect=csv.excel)
	for mrt in masterToutrows:
		TRwriter.writerow(mrt)
	TR.close()
	
	UR=open(masterUoutname, 'w')
	URwriter=csv.writer(UR, dialect=csv.excel)
	for mut in masterUoutrows:
		URwriter.writerow(mut)
	UR.close()
	
