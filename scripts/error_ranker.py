#!/usr/bin/env python

## 2015/09/20. LK. Error ranker. This operates on the output of compare_tfidf_vectors.py.

import sys, os, csv

def get_score(myarg):
	with open(myarg) as mycsv:
		myreader = csv.reader(mycsv, delimiter=',')
		myreader.next() ##skip over the header row
		scoredict = {}
		rank = 1
		score = 0
		errcount = 0
		for row in myreader:
			if row[0] in scoredict:
				scoredict[row[0]].append((rank, row[1], row[2], row[3]))
			else:
				scoredict[row[0]]=[(rank, row[1], row[2], row[3])]
			rank+=1
		for k in scoredict:
			ranksum = 0
			sdkval = scoredict[k]
			for v in sdkval:
				ranksum += v[0]
			rankavg = float(ranksum / len(sdkval))
			for v in sdkval:
				if v[3].strip() in ['form', 'triple']:
					score += rankavg
					errcount += 1
	return score, errcount
				
def main():
	if not os.path.exists('exp_Raw_scores'):
		os.makedirs('exp_Raw_scores')
	allscores = {}
	testitems=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	forms=['ldh', 'ldx', 'xdh', 'lxh', 'xdx']
	versions=['NNSO', 'NNSLM']
	goldrefs = ['GS_B', 'GS_W']
	testgoldrefs = ['NNSO_B_v_GS_B', 'NNSO_W_v_GS_W', 'NNSLM_B_v_GS_B', 'NNSLM_W_v_GS_W']	
	for testitem in testitems:
		tiscores = []
		ticsvname = 'i'+testitem+'exp_Raw_scores.csv'
		ticsv = open('exp_Raw_scores/'+ticsvname, 'w')
		ticsvwriter = csv.writer(ticsv)
		ticsvheadrow = ['error_score', 'experiment', 'error_count']
		ticsvwriter.writerow(ticsvheadrow)
		for tgr in testgoldrefs:
			for form in forms:
				mgroupname = 'TC_'+tgr+'_'+form
				mexpname = 'i'+testitem+'_TC_'+tgr+'_'+form
				mfilearg = 'exp_csv/'+mexpname+'.csv'
				mexpscore, mexperr = get_score(mfilearg)
				tiscores.append((mexpscore, mexpname, mexperr))
				if mgroupname in allscores:
					allscores[mgroupname]+=mexpscore
				else:
					allscores[mgroupname] = mexpscore
		for ver in versions:
			for gr in goldrefs:
				for form in forms:
					agroupname = 'TA_'+ver+'_v_'+gr+'_'+form
					aexpname = 'i'+testitem+'_TA_'+ver+'_v_'+gr+'_'+form
					afilearg = 'exp_csv/'+aexpname+'.csv'
					aexpscore, aexperr = get_score(afilearg)
					tiscores.append((aexpscore, aexpname, aexperr))
					if agroupname in allscores:
						allscores[agroupname]+=aexpscore
					else:
						allscores[agroupname] = aexpscore
		for ver in versions:
			# lgroupname = 'FA_'+ver+'_lemma'
			# lexpname = 'i'+testitem+'_FA_'+ver+'_lemma'
			# lfilearg = 'exp_csv/'+lexpname+'.csv'
			# lexpscore, lexperr = get_score(lfilearg)
			# tiscores.append((lexpscore, lexpname, lexperr))
			# if lgroupname in allscores:
			# 	allscores[lgroupname]+=lexpscore
			# else:
			# 	allscores[lgroupname] = lexpscore
			for form in forms:
				bgroupname = 'FA_'+ver+'_'+form
				bexpname = 'i'+testitem+'_FA_'+ver+'_'+form
				bfilearg = 'exp_csv/'+bexpname+'.csv'
				bexpscore, bexperr = get_score(bfilearg)
				tiscores.append((bexpscore, bexpname, bexperr))
				if bgroupname in allscores:
					allscores[bgroupname]+=bexpscore
				else:
					allscores[bgroupname] = bexpscore

		for ver in versions:
			# clgroupname = 'FC_'+ver+'_lemma'
			# clexpname = 'i'+testitem+'_FC_'+ver+'_lemma'
			# clfilearg = 'exp_csv/'+clexpname+'.csv'
			# clexpscore, clexperr = get_score(clfilearg)
			# tiscores.append((clexpscore, clexpname, clexperr))
			# if clgroupname in allscores:
			# 	allscores[clgroupname]+=clexpscore
			# else:
			# 	allscores[clgroupname] = clexpscore
			for form in forms:
				cgroupname = 'FC_'+ver+'_'+form
				cexpname = 'i'+testitem+'_FC_'+ver+'_'+form
				cfilearg = 'exp_csv/'+cexpname+'.csv'
				cexpscore, cexperr = get_score(cfilearg)
				tiscores.append((cexpscore, cexpname, cexperr))
				if cgroupname in allscores:
					allscores[cgroupname]+=cexpscore
				else:
					allscores[cgroupname] = cexpscore

		tiscores.sort(cmp=None, key=None, reverse=False)
		for ticsvrow in tiscores:
			ticsvwriter.writerow(ticsvrow)
		ticsv.close()
	allscoreslist = []
	for ak in allscores:
		allscoreslist.append([allscores[ak], ak])
	allscoreslist.sort(cmp=None, key=None, reverse=False)
	allcsvname = 'all_exp_Raw_scores.csv'
	allcsv = open('exp_Raw_scores/'+allcsvname, 'w')
	allcsvwriter = csv.writer(allcsv)
	allcsvheadrow = ['avg_err_score', 'experiment']
	allcsvwriter.writerow(allcsvheadrow)
	for apair in allscoreslist:
		writepair = [(apair[0]/10), apair[1]]
		allcsvwriter.writerow(writepair)
	allcsv.close()

if __name__ == "__main__":
    main()

