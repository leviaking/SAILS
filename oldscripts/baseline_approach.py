#!/usr/bin/env python

## 2015/09/01. LK. This script is a companion to "compare_tfidf_vectors.py" and really should be incorporated into that script. This script applies the baseline approach (a NNS sentence is scored & ranked according to its baseline score; for each "term" in the NNS test sentence (here, that's a lemma or a dependency string), we find that term's relative frequency in the gold standard; we sum up these relative frequencies, then divide by the number of terms in the test sentence to get the average term score, and this becomes the baseline score for that sentence).
## USAGE: python baseline_approach.py test_directory gold_directory
##The "test_directory" (arg1) should be the name of the folder containing the subfolders of txt/ xml/ ldh/ ldx/ etc. containing the test material, and gold_directory should be the equivalent folder for the NS gold standard. For our purposes, this will most likely be "GS". NOTE that this is different from the "gold_directory" of compare_tfidf_vectors.py, where the gold_directory is "wsj" or "brown".

import sys, os, csv

def get_test_sentence_text(td, ti, pt):
	sentname = td+'/txt/i'+ti+'p'+pt+'.txt'
	sentfile = open(sentname, 'r')
	sent = sentfile.readlines()[0].strip() ##sent is now the actual text of the sentence.
	sentfile.close()
	return sent

def get_test_text_or_depstrings(td, f, ti, pt):
	fn = td+'/'+f+'/'+'i'+ti+'p'+pt+'.'+f
	fi = open(fn, 'r')
	sentstring = fi.readlines()[0].strip()
	fi.close()
	return sentstring

def get_baseline_columns_lemma(td, ti): ###NOTE2. WORKING HERE... (definition is not finished)
	col_pairs = []
	#lemmapair = get_baseline_lemma_col_pair() ## (score, sentence)
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
	for key in goldtokendict:
		goldtokenstotal += goldtokendict[key]
	for gkey in goldtokendict:
		goldtokendict[gkey] = float(goldtokendict[key]/goldtokenstotal) ##goldtokendict is now {lemma: relative_frequency}
	for px in range (1,40):
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tlem_in = open(td+'/lemma_conll/i'+ti+'p'+participant+'.lemma_conll', 'r')
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
			if tlemma in goldtokendict:
				tscore += goldtokendict[tlemma]
			else: pass
		tscore = float(tscore/ len(tlemmas))
		col_pairs.append((tscore, psent))
	col_pairs.sort(cmp=None, key=None, reverse=True)
	return col_pairs

#get_baseline_columns_depstrings(testdir, testitem, f)
def get_baseline_columns_depstrings(td, ti, f):
	col_pairs = []
	#lemmapair = get_baseline_lemma_col_pair() ## (score, sentence)
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
	#goldlines = filter(None, goldlines)
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
	for px in range (1,40):
		participant =  str(px).zfill(2)
		psent = get_test_sentence_text(td, ti, participant)
		tdepstr_in = open(td+'/'+f+'/i'+ti+'p'+participant+'.'+f, 'r')
		tdepstr_line = tdepstr_in.readline()
		tdepstr_in.close()
		tdepstrs = tdepstr_line.split()
		tscore = float(0)
		for tds in tdepstrs:
			if tds in goldtokendict:
				tscore += goldtokendict[tds]
			else: pass
		tscore = float(tscore/ len(tdepstrs))
		col_pairs.append((tscore, psent))
	col_pairs.sort(cmp=None, key=None, reverse=True)
	return col_pairs

####MAIN PROGRAM
def main():
	testdir=sys.argv[1]
	#golddirlist=all_sys_args[2:] ##['wsj', 'brown']
	testitems=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	forms=['ldh', 'ldx', 'xdh', 'lxh']
	all_gfnames = ['base_lemma', 'base_ldh', 'base_ldx', 'base_xdh', 'base_lxh']
	headrow=['base_lemma_rf', 'base_lemma_sent', 'base_ldh_rf', 'base_ldh_sent', 'base_ldx_rf', 'base_ldx_sent', 'base_xdh_rf', 'base_xdh_sent', 'base_lxh_rf', 'base_lxh_sent']
	all_csvs = []
	for testitem in testitems: ##this loop gets a sorted list of tuples (cosine, sentence) representing a pair of csv columns, for each set of test parameters.
		all_col_pair_dict = {}
		lemma_col_pairs = get_baseline_columns_lemma(testdir, testitem) ##[(score, sentence), ...]
		all_col_pair_dict['base_lemma'] = lemma_col_pairs
		#print lemma_col_pairs
		for form in forms:
			fname = 'base_'+form
			depstring_col_pairs = get_baseline_columns_depstrings(testdir, testitem, form)
			#gfname = gold+'_'+form
			#sorted_col_pairs = get_col_pairs_for_all_participants(testdir, testitem, gold, form) ###this is all the cosine-sentence pairs for the given form-gold combination
			all_col_pair_dict[fname]=depstring_col_pairs
		onecsv=[]
		for gf in all_gfnames:
			onecsv.append(all_col_pair_dict[gf])
		all_csvs.append(onecsv)
	while all_csvs: ##this loop assembles rows from the csv columns, and writes rows to files.
		curr_cvs_data = all_csvs.pop(0)
		curr_item = testitems.pop(0)
		itemcsvname='i'+curr_item+'baseline_ranked.csv'
		itemcsv = open(itemcsvname, 'w')
		itemcsvwriter=csv.writer(itemcsv)
		itemcsvwriter.writerow(headrow)
		ziprows = zip(*curr_cvs_data)
		for datarow in ziprows:
			printrow = []
			for datapair in datarow:
				for datum in datapair:
					printrow.append(datum)
			itemcsvwriter.writerow(printrow)
		itemcsv.close()

if __name__ == "__main__":
    main()
