#!/usr/bin/env python

## 2015/04/04. I changed the script so that output files now reflect the model names we use in the 2016 BEA paper: the original names (a, b, c, m) become TA, FA, FC, TC respectively.

## 2015/08/15. LK. We will have two sets of tfidf scores. Each set is a list of "terms" of the form label$@%dependent$@%head, followed by a tab and a score, e.g., 0.0103214220104. One entry per line. There will be some overlap, but we expect each set to have unique terms. So we first need to get the union of the two sets. For each set, any of these missing terms should be added with a score of 0. Then we sort the sets by term so they are in the same order, then make a list (vector) of the corresponding scores and calculate the cosine similarity.
## USAGE: python sentence_rankings.py test_results gold_results ###This is for generating a .csv file for each comparison. The "test_results" and "gold_results" should be the names of the folders output by lk_tfidf.py. All output from this script will go in the "exp_csv" folder. At this point, in order to get the full set of rankings, this script needs to be run 4 times:
##python sentence_rankings.py NNSO_brown_tfidf GS_brown_tfidf
##python sentence_rankings.py NNSO_wsj_tfidf GS_wsj_tfidf
##python sentence_rankings.py NNSLM_brown_tfidf GS_brown_tfidf
##python sentence_rankings.py NNSLM_wsj_tfidf GS_wsj_tfidf

## 2015/10/5. renamed from compare_tfidf_vectors.py

import sys, os, csv
from scipy.spatial.distance import cosine
all_sys_args = [sys.argv[1], sys.argv[2]]

def get_pairlist_from_text(arg):
	my_in=open(arg, 'r')
	mytext=my_in.read()
	my_in.close()
	mytext = mytext.strip()
	mylist = mytext.split('\n')
	mypairs = []
	for l in mylist:
		pair = l.split('\t')
		mypair = [pair[0], float(pair[1])] ###['det$@%the$@%ball ', 0.000612366102979]
		mypairs.append(mypair)
	return mypairs ###[['det$@%the$@%ball ', 0.000612366102979], ['dobj$@%football$@%kick ', 0.00061635392412] ...]

def get_strings_from_tfidf_results(arg):
	my_in=open(arg, 'r')
	mytext=my_in.read()
	my_in.close()
	mytext = mytext.strip()
	mylist = mytext.split('\n')
	mystrings = []
	for l in mylist:
		mystring = l.split('\t')[0] ###'root$@%shoot$@%VROOT'
		mystrings.append(mystring)
	return mystrings ###['det$@%a$@%man', 'root$@%shoot$@%VROOT', 'punct$@%.$@%shoot']

def get_union(x, y):
	myunion = []
	for i in x:
		myunion.append(i[0])
	for j in y:
		if j[0] not in myunion:
			myunion.append(j[0])
	return myunion ###['det$@%x$@%man ', 'nsubj$@%x$@%shoot ', 'dobj$@%x$@%shoot ', ...]
	
def add_missing_terms(u, g, t):
	gterms=[]
	for k in g:
		gterms.append(k[0])
	tterms=[]
	for l in t:
		tterms.append(l[0])
	newg=list(g)
	newt=t[:]
	for m in u:
		if m not in gterms:
			newg.append([m, float(0.0)])
		else: pass
		if m not in tterms:
			newt.append([m, float(0.0)])
		else: pass
	return newg, newt ###[['root$@%ride$@%VROOT ', 0.00228021380125], ['punct$@%.$@%ride ', 0.00228021380125], ...] ###newg & newt are identical in format, but the number values should differ.
		
def get_scores_lists(g, t):
	gsl=[]
	tsl=[]
	for i in g:
		gsl.append(i[1])
	for j in t:
		tsl.append(j[1])
	return gsl, tsl ###[0.000612044036513, 0.00102208794732, 0.0, ...] ###gsl & tsl are identical format, but there will usually be more zeros in tsl.

def get_single_cosine(targ, garg):
	gspairs = get_pairlist_from_text(garg)
	tpairs = get_pairlist_from_text(targ)
	union = get_union(gspairs, tpairs)
	gsfull, tfull = add_missing_terms(union, gspairs, tpairs)
	gsfull.sort()
	tfull.sort()
	gsscores, tscores = get_scores_lists(gsfull, tfull)
	mycosine = cosine(tscores, gsscores)
	return mycosine ###0.169940096113

def get_test_sentence_text(td, ti, pt):
	tsource = td.split('_')[0]
	sentname = tsource+'/txt/i'+ti+'p'+pt+'.txt'
	sentfile = open(sentname, 'r')
	sent = sentfile.readlines()[0].strip() ##sent is now the actual text of the sentence.
	sentfile.close()
	return sent ###A guy is painting a girl's portrait.

def get_col_pairs_for_all_participants(td, ti, g, f, md):
	col_pairs = []
	tsource = td.split('_')[0].strip()
	refcorp = g.split('_')[1]
	goldvectorarg = g+'/i'+ti+'gs.'+f+'_'+refcorp+'.tfidf' ##'GS_wsj_tfidf/i01gs.ldh_wsj.tfidf
	for px in range (1,40):
		participant =  str(px).zfill(2)
		testvectorarg = td+'/i'+ti+'p'+participant+'.'+f+'_'+refcorp+'.tfidf' ##'NNS_wsj_tfidf/i01p01.ldh_wsj.tfidf'
		psent = get_test_sentence_text(td, ti, participant)
		mycosine = get_single_cosine(testvectorarg, goldvectorarg)
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		col_pairs.append((mycosine, psent, ttrip, terr))
	col_pairs.sort(cmp=None, key=None, reverse=True) #9/22
	return col_pairs ###[(0.16994009611317018, 'A man shot a bird.'), ... (0.99840888509639625, 'Man pull bird.')]

def get_baseline_columns_lemma(td, ti, md): 
	col_pairs = []
	tsource = td.split('_')[0].strip()
	goldtextin = open('GS/lemma_conll/i'+ti+'gs.lemma_conll', 'r') ##'GS/lemma_conll/i01gs.lemma_conll'
	goldlines = goldtextin.readlines()
	goldtextin.close()
	goldlines = filter(None, goldlines)
	goldtokendict = {}
	for gl in goldlines:
		if not gl.strip() == '':
			lem = gl.split('\t')[1]
			if lem not in goldtokendict:
				goldtokendict[lem] = float(1)
			else:
				goldtokendict[lem] += float(1)
		else: pass
	goldtokenstotal = 0
	goldtypestotal = 0
	for key in goldtokendict:
		goldtokenstotal += goldtokendict[key]
		goldtypestotal += 1
	for gkey in goldtokendict:
		goldtokendict[gkey] = float(goldtokendict[key]/goldtokenstotal) ##goldtokendict is now {lemma: relative_frequency}
	allparticipantstokens = []
	for px in range (1,40):
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tlem_in = open(tsource+'/lemma_conll/i'+ti+'p'+participant+'.lemma_conll', 'r')
		tlem_lines = tlem_in.readlines()
		tlem_in.close()
		tlem_lines = filter(None, tlem_lines)
		tlemmas = []
		for tll in tlem_lines:
			if tll.strip() == '':
				pass
			else:
				tlem = tll.split('\t')[1]
				tlemmas.append(tlem)
		tscore = float(0)
		for tlemma in tlemmas:
			allparticipantstokens.append(tlemma)
			if tlemma in goldtokendict:
				tscore += goldtokendict[tlemma]
			else: pass
		tscore = float(tscore/ len(tlemmas))
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		col_pairs.append((tscore, psent, ttrip, terr))
	col_pairs.sort()
	totalparticipantstokens = len(allparticipantstokens)
	allparticipantstypes = []
	for token in allparticipantstokens:
		if token not in allparticipantstypes:
			allparticipantstypes.append(token)
	totalparticipantstypes = len(allparticipantstypes)
	#print str(totalparticipantstokens)+'/'+str(totalparticipantstypes)
	#print str(goldtokenstotal)+'/'+str(goldtypestotal)
	return col_pairs

def get_baseline_columns_depstrings(td, ti, f, md):
	col_pairs = []
	tsource = td.split('_')[0]
	goldtextin = open('GS/'+f+'/i'+ti+'gs.'+f, 'r') ##'GS/ldh/i01gs.ldh'
	goldlines = goldtextin.readlines()
	goldtextin.close()
	goldbag = []
	for gl in goldlines:
		gl = gl.strip()
		if not gl == '':
			gl = gl.split()
			for glstr in gl:
				goldbag.append(glstr)
		else: pass
	goldtokendict = {}
	for gtoken in goldbag:
		if gtoken not in goldtokendict:
			goldtokendict[gtoken] = float(1)
		else:
			goldtokendict[gtoken] += float(1)
	goldtokenstotal = float(0)
	goldtypestotal = float(0)
	for key in goldtokendict:
		goldtypestotal += 1
		goldtokenstotal += goldtokendict[key]
	for gkey in goldtokendict:
		goldtokendict[gkey] = float(goldtokendict[key]/goldtokenstotal) ##goldtokendict is now {depstring: rel_freq}
	for px in range (1,40):
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tdepstr_in = open(tsource+'/'+f+'/i'+ti+'p'+participant+'.'+f, 'r')
		tdepstr_line = tdepstr_in.readline()
		tdepstr_in.close()
		tdepstrs = tdepstr_line.split()
		tscore = float(0)
		for tds in tdepstrs:
			if tds in goldtokendict:
				tscore += goldtokendict[tds]
			else: pass
		tscore = float(tscore/ len(tdepstrs))
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		col_pairs.append((tscore, psent, ttrip, terr))
	col_pairs.sort()
	return col_pairs

def get_clem_col_pairs(td, ti, md):
	ccol_pairs = []
	tsource = td.split('_')[0].strip()
	goldtextin = open('GS/lemma_conll/i'+ti+'gs.lemma_conll', 'r') ##'GS/lemma_conll/i01gs.lemma_conll'
	goldlines = goldtextin.readlines()
	goldtextin.close()
	goldlines = filter(None, goldlines)
	goldtokendict = {}
	for gl in goldlines:
		if not gl.strip() == '':
			lem = gl.split('\t')[1]
			if lem not in goldtokendict:
				goldtokendict[lem] = float(1)
			else:
				goldtokendict[lem] += float(1)
		else: pass
	goldtokenstotal = float(0)
	goldtypestotal = float(0)
	for key in goldtokendict:
		goldtokenstotal += goldtokendict[key]
		goldtypestotal += 1
	for gkey in goldtokendict:
		goldtokendict[gkey] = float(goldtokendict[key]/goldtokenstotal) ##goldtokendict is now {lemma: relative_frequency}
	goldpairs = []
	for gkey in goldtokendict:
		goldpairs.append([gkey, goldtokendict[gkey]])
	goldpairs.sort()
	allparticipantstokens = []
	for px in range (1,40):
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tlem_in = open(tsource+'/lemma_conll/i'+ti+'p'+participant+'.lemma_conll', 'r')
		tlem_lines = tlem_in.readlines()
		tlem_in.close()
		tlem_lines = filter(None, tlem_lines)
		tlemmas = []
		for tll in tlem_lines:
			if tll.strip() == '':
				pass
			else:
				tlem = tll.split('\t')[1]
				tlemmas.append(tlem)
		tlemmadict = {}
		for tlemma in tlemmas:
			allparticipantstokens.append(tlemma)
			if tlemma not in tlemmadict:
				tlemmadict[tlemma] = float(1)
			else:
				tlemmadict[tlemma] += float(1)
		tlemmastotal = float(0)
		for tkey in tlemmadict:
			tlemmastotal += tlemmadict[tkey]
		for tlkey in tlemmadict:
			tlemmadict[tlkey] = float(tlemmadict[tlkey]/tlemmastotal) ## tlemmadict is now {lemma: relative_frequency}
		tpairs = []
		for tk in tlemmadict:
			tpairs.append([tk, tlemmadict[tk]])
		tpairs.sort()
		tscore = float(0)
		union = get_union(goldpairs, tpairs)
		gsfull, tfull = add_missing_terms(union, goldpairs, tpairs)
		gsfull.sort()
		tfull.sort()
		gsscores, tscores = get_scores_lists(gsfull, tfull)
		ccosine = cosine(tscores, gsscores)
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		ccol_pairs.append((ccosine, psent, ttrip, terr))
	ccol_pairs.sort(cmp=None, key=None, reverse=True) #9/22
	totalparticipantstokens = len(allparticipantstokens)
	allparticipantstypes = []
	for token in allparticipantstokens:
		if token not in allparticipantstypes:
			allparticipantstypes.append(token)
	totalparticipantstypes = len(allparticipantstypes)
	#print totalparticipantstokens, totalparticipantstypes
	return ccol_pairs ###[(0.16994009611317018, 'A man shot a bird.'), ... (0.99840888509639625, 'Man pull bird.')]

def get_charlie_columns_depstrings(td, ti, f, md):
	ccol_pairs = []
	tsource = td.split('_')[0]
	goldtextin = open('GS/'+f+'/i'+ti+'gs.'+f, 'r') ##'GS/ldh/i01gs.ldh'
	goldlines = goldtextin.readlines()
	goldtextin.close()
	goldbag = []
	for gl in goldlines:
		gl = gl.strip()
		if not gl == '':
			gl = gl.split()
			for glstr in gl:
				goldbag.append(glstr)
		else: pass
	goldtokendict = {}
	for gtoken in goldbag:
		if gtoken not in goldtokendict:
			goldtokendict[gtoken] = float(1)
		else:
			goldtokendict[gtoken] += float(1)
	goldtokenstotal = float(0)
	for key in goldtokendict:
		goldtokenstotal += goldtokendict[key]
	for gkey in goldtokendict:
		goldtokendict[gkey] = float(goldtokendict[key]/goldtokenstotal) ##goldtokendict is now {depstring: rel_freq}
	goldpairs = []
	for gkey in goldtokendict:
		goldpairs.append([gkey, goldtokendict[gkey]])
	goldpairs.sort()
	for px in range (1,40):
		tbag = []
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tdepstr_in = open(tsource+'/'+f+'/i'+ti+'p'+participant+'.'+f, 'r')
		tdepstr_line = tdepstr_in.readline()
		tdepstr_in.close()
		tdepstrs = tdepstr_line.split()
		tdepstrs = filter(None, tdepstrs)
		for tdepstr in tdepstrs:
			tbag.append(tdepstr)
		ttokensdict = {}
		for ttoken in tbag:
			if ttoken not in ttokensdict:
				ttokensdict[ttoken] = float(1)
			else:
				ttokensdict[ttoken] += float(1)
		ttokenstotal = float(0)
		for tk in ttokensdict:
			ttokenstotal += ttokensdict[tk]
		for tke in ttokensdict:
			ttokensdict[tke] = float(ttokensdict[tke]/ttokenstotal) ##ttokensdict is now {depstring: rel_freq}
		tpairs = []
		for tkey in ttokensdict:
			tpairs.append([tkey, ttokensdict[tkey]])
		tpairs.sort()
		union = get_union(goldpairs, tpairs)
		gsfull, tfull = add_missing_terms(union, goldpairs, tpairs)
		gsfull.sort()
		tfull.sort()
		gsscores, tscores = get_scores_lists(gsfull, tfull)
		ccosine = cosine(tscores, gsscores)
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		ccol_pairs.append((ccosine, psent, ttrip, terr))
	ccol_pairs.sort(cmp=None, key=None, reverse=True) #9/22
	return ccol_pairs ###[(0.16994009611317018, 'A man shot a bird.'), ... (0.99840888509639625, 'Man pull bird.')]

def get_alpha_columns(td, ti, g, f, md):
	tsource = td.split('_')[0]
	col_pairs = []
	refcorp = g.split('_')[1]
	goldvectorarg = g+'/i'+ti+'gs.'+f+'_'+refcorp+'.tfidf' ##'GS_wsj_tfidf/i01gs.ldh_wsj.tfidf'
	for px in range (1,40):
		participant =  str(px).zfill(2)
		testvectorarg = td+'/i'+ti+'p'+participant+'.'+f+'_'+refcorp+'.tfidf' ##'NNS_wsj_tfidf/i01p01.ldh_wsj.tfidf'
		psent = get_test_sentence_text(td, ti, participant) ##used for printing (visual reference) only, not in processing here.
		myalpha = get_single_alpha(testvectorarg, goldvectorarg)
		ttrip, terr = md[participant][tsource][1], md[participant][tsource][2]
		col_pairs.append((myalpha, psent, ttrip, terr))
	#col_pairs.sort(cmp=None, key=None, reverse=True)
	col_pairs.sort(cmp=None, key=None)
	return col_pairs

def get_single_alpha(targ, garg):
	gspairs = get_pairlist_from_text(garg)
	tstrings = get_strings_from_tfidf_results(targ)
	gd = {} ##{GS_string : GS_tfidf_score, ...}
	for gp in gspairs:
		if gp[0] not in gd:
			gd[gp[0]] = gp[1]
	running_total = float(0)
	for ts in tstrings:
		if ts in gd:
			running_total += gd[ts]
	mylength = float(len(tstrings))
	alpha_avg = running_total/mylength
	return alpha_avg

def get_mappings(ti):
	md = {}
	with open('NNS_mappings/i'+ti+'mapping.csv') as mapcsv:
		mapreader = csv.reader(mapcsv, delimiter=',')
		mapreader.next() ##skip over the header row
		for row in mapreader:
			versiondict = {}
			versiondict['NNSO'] = (row[1].strip(), row[3].strip(), row[5].strip())
			versiondict['NNSLM'] = (row[2].strip(), row[4].strip(), row[6].strip())
			md[str(int(row[0].strip())).zfill(2)] = versiondict
	return md

def main():
	if not os.path.exists('exp_csv'):
		os.makedirs('exp_csv')
	testdir=all_sys_args[0]
	testversion = testdir.split('_')[0].strip() ##This should be "NNSO" or "NNSLM"
	testref = testdir.split('_')[1].strip()
	if testref == 'brown':
		testref = 'B'
	elif testref == 'wsj':
		testref = 'W'
	else:
		pass
	gold=all_sys_args[1]
	testitems=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	forms=['ldh', 'ldx', 'xdh', 'lxh', 'xdx']
	for testitem in testitems: ##this loop gets a sorted list of tuples (cosine, sentence) representing a pair of csv columns, for each set of test parameters.
		mapdict = get_mappings(testitem) ### {'01': {'NNSO': (<sent>, <triple>, <error>), 'NNSLM': ( ...)}, '02': ... }
		###NOTE that the "lemma" stuff here is actually part of the baseline measures but must be handled differently.
		lemma_col_pairs = get_baseline_columns_lemma(testdir, testitem, mapdict) ##[(score, sentence), ...]
		#lemma_csv_name = 'i'+testitem+'_b_'+testversion+'_lemma'
		lemma_csv_name = 'i'+testitem+'_FA_'+testversion+'_lemma'
		lemma_csv = open('exp_csv/'+lemma_csv_name+'.csv', 'w')
		lemma_csv_writer = csv.writer(lemma_csv)
		lemma_head_row = [lemma_csv_name+'_rf', lemma_csv_name+'_sent', lemma_csv_name+'_triple', lemma_csv_name+'_err']
		lemma_csv_writer.writerow(lemma_head_row)
		for lp in lemma_col_pairs:
			lemma_row = [lp[0], lp[1], lp[2], lp[3]]
			lemma_csv_writer.writerow(lemma_row)
		lemma_csv.close()
		###We need a "charlie" lemma section here.
		clem_col_pairs = get_clem_col_pairs(testdir, testitem, mapdict)
		#clem_csv_name = 'i'+testitem+'_c_'+testversion+'_lemma'
		clem_csv_name = 'i'+testitem+'_FC_'+testversion+'_lemma'
		clem_csv = open('exp_csv/'+clem_csv_name+'.csv', 'w')
		clem_csv_writer = csv.writer(clem_csv)
		clem_head_row = [clem_csv_name+'_rf_cos', clem_csv_name+'_sent', clem_csv_name+'_triple', clem_csv_name+'_err']
		clem_csv_writer.writerow(clem_head_row)
		for clp in clem_col_pairs:
			clem_row = [clp[0], clp[1], clp[2], clp[3]]
			clem_csv_writer.writerow(clem_row)
		clem_csv.close()
		for form in forms:
			depstring_col_pairs = get_baseline_columns_depstrings(testdir, testitem, form, mapdict) #
			#base_csv_name = 'i'+testitem+'_b_'+testversion+'_'+form
			base_csv_name = 'i'+testitem+'_FA_'+testversion+'_'+form
			base_csv = open('exp_csv/'+base_csv_name+'.csv', 'w')
			base_csv_writer = csv.writer(base_csv)
			base_head_row = [base_csv_name+'_rf', base_csv_name+'_sent', base_csv_name+'_triple', base_csv_name+'_err']
			base_csv_writer.writerow(base_head_row)
			for bp in depstring_col_pairs:
				base_row = [bp[0], bp[1], bp[2], bp[3]]
				base_csv_writer.writerow(base_row)
			base_csv.close()
			###Approach C ("charlie") goes here.
			charlie_col_pairs = get_charlie_columns_depstrings(testdir, testitem, form, mapdict)
			#charlie_csv_name = 'i'+testitem+'_c_'+testversion+'_'+form
			charlie_csv_name = 'i'+testitem+'_FC_'+testversion+'_'+form
			charlie_csv = open('exp_csv/'+charlie_csv_name+'.csv', 'w')
			charlie_csv_writer = csv.writer(charlie_csv)
			charlie_head_row = [charlie_csv_name+'_rf_cos', charlie_csv_name+'_sent', charlie_csv_name+'_triple', charlie_csv_name+'_err']
			charlie_csv_writer.writerow(charlie_head_row)
			for cp in charlie_col_pairs:
				charlie_row = [cp[0], cp[1], cp[2], cp[3]]
				charlie_csv_writer.writerow(charlie_row)
			charlie_csv.close()
			###
			gnamelistthing = gold.split('_')
			if gnamelistthing[1] in ['brown', 'B']:
				gnamevar = gnamelistthing[0]+'_B_'
			elif gnamelistthing[1] in ['wsj', 'W']:
				gnamevar = gnamelistthing[0]+'_W_'
			sorted_col_pairs = get_col_pairs_for_all_participants(testdir, testitem, gold, form, mapdict) ###this is all the cosine-sentence pairs for the given form-gold combination
			#exp_csv_name = 'i'+testitem+'_m_'+testversion+'_'+testref+'_v_'+gnamevar+form
			exp_csv_name = 'i'+testitem+'_TC_'+testversion+'_'+testref+'_v_'+gnamevar+form
			exp_csv = open('exp_csv/'+exp_csv_name+'.csv', 'w')
			exp_csv_writer = csv.writer(exp_csv)
			exp_head_row = [exp_csv_name+'_cos', exp_csv_name+'_sent', exp_csv_name+'_triple', exp_csv_name+'_err']
			exp_csv_writer.writerow(exp_head_row)
			for pair_tuple in sorted_col_pairs:
				exp_row = [pair_tuple[0], pair_tuple[1], pair_tuple[2], pair_tuple[3]]
				exp_csv_writer.writerow(exp_row)
			exp_csv.close()
			sorted_alpha_col_pairs = get_alpha_columns(testdir, testitem, gold, form, mapdict)
			#exp_csv_name = 'i'+testitem+'_m_'+testversion+'_'+testref+'_v_'+gnamevar+form+'.csv'
			#exp_csv_name = 'i'+testitem+'_IC_'+testversion+'_'+testref+'_v_'+gnamevar+form+'.csv'
			#a_csv_name = 'i'+testitem+'_a_'+testversion+'_v_'+gnamevar+form
			a_csv_name = 'i'+testitem+'_TA_'+testversion+'_v_'+gnamevar+form
			a_csv = open('exp_csv/'+a_csv_name+'.csv', 'w')
			a_csv_writer = csv.writer(a_csv)
			a_head_row = [a_csv_name+'_score', a_csv_name+'_sent', a_csv_name+'_triple', a_csv_name+'_err']
			a_csv_writer.writerow(a_head_row)
			for pair_tuple in sorted_alpha_col_pairs:
				a_row = [pair_tuple[0], pair_tuple[1], pair_tuple[2], pair_tuple[3]]
				a_csv_writer.writerow(a_row)
			a_csv.close()

if __name__ == "__main__":
    main()
