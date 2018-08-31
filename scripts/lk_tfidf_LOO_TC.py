#!/usr/bin/env python

##2018-08-14. LK. This script takes an output file from prep_conll_for_tfidf.py / prep_conll_for_tfidf.sh. So far, those output files have been like this: each one represents a particular gold standard (e.g., "all native responses" or "all crowdsourced native responses", etc.) for a particular item (e.g., item 1 untargeted, or item 19 targeted). Each file is a csv, where the columns are like so (this is the header):
##ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx
##(obvious)		(These five are annotation: "1" or "0")				(lemmatized CoNNL parse (multiline cell))	(ldh, etc. are "depstrings"--each dependency is a concatenated string with a delimiter symbol)
##
##This also relies on a reference corpus; here, I use the Brown corpus, and the documents in the corpus have been prepared as depstrings; there are separate versions for ldh, xdh and xdx.
##
##This script iterates over each response in the file; in a given iteration, it pulls out response X to be the test response, and composes a new GS, let's call it "GS^X", which contains all responses in the file *except* X. In other words, this script performs leave-one-out testing on each response. It scores each response using the "TC" tf-idf cosine method described in King and Dickinson 2016. TC takes the GS and gives each term (depstring) a tf-idf score via the reference corpus. Then it does the same for the test response. It creates a union list of the terms in the GS and the test response, sorts it, then creates a corresponding GS vector with the GS tf-idf scores, and a test vector with the corresponding test tf-idf scores. It then calculates the cosine of these two vectors, resulting in a single score for the test response, which represents the test response distance from the GS.
##The output is a csv, where the first 11 columns are identical to the input csv, and the next three columns are the TC score for ldh, xdh and xdx depstrings. This file is the same filename as the input, with "depstrings.csv" replaced with "LOO_TC.csv"; the output file is stored in a sister folder to the input file folder, called "LOO_TC".
##
##USAGE:
##python lk_tfidf_LOO_TC.py inputfile ###inputfile is e.g., "../gold_standards/depstrings/I01T_all_fns_depstrings.csv"
##
##This script is intended to be run via the lk_tfidf_TC.sh shell, which will iterate through all files in the "depstrings" folder.

import sys, math, csv
from os import walk
from scipy.spatial.distance import cosine

testdocfn = sys.argv[1]
if '/' in testdocfn:
	testdocfn=testdocfn.split('/')[-1]
else:
	pass
gsdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/')
sourcedir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/depstrings/')
#mycorpusdir = sys.argv[2]
mycorpusdir=('/Users/leviking/Documents/dissertation/SAILS_annex/brown/')
outputdir=('/Users/leviking/Documents/dissertation/SAILS/gold_standards/LOO_TC/')
depcols={'ldh':8, 'xdh':9, 'xdx':10} ##the columns where each deptype is stored

def get_refdoc_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	return docnames

def get_word_list(somedoc, d):
	wds = []
	with open(mycorpusdir+d+'/'+somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for w in clist:
				wds.append(w)
	return wds

def build_ref_wordlists():
	dtwordlists={}
	dts=['ldh', 'xdh', 'xdx']
	for dt in dts:
		myrefdocs = get_refdoc_names(mycorpusdir+dt) ##this is the refernce corpus
		docwordlists=[]
		for refdoc in myrefdocs:
			reftokens = get_word_list(refdoc, dt)
			docwordlists.append(reftokens)
		dtwordlists[dt]=docwordlists
	return dtwordlists ##{'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}

def get_source_content(tdf):
	everything=[]
	tdoc=open(sourcedir+tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything

def get_current_split(allinput, c):
	cgsrows=[]
	ctestrow=allinput[c]
	front=allinput[:c]
	back=allinput[int(c)+1:]
	if front:
		cgsrows.append(front)
	else: pass
	if back:
		cgsrows.append(back)
	else: pass
	return ctestrow, cgsrows

# def add_to_table(currdoc, tbl):
# 	tbl.addDocument(currdoc, get_word_list(currdoc))
# 	return tbl

def get_test_tokens(trow, dt):
	tts = trow[depcols[dt]]
	return tts

def get_gs_tokens(gsrows, dty):
	gsts=[]
	for gr in gsrows:
		#print 'gr: ', gr
		for r in gr:
			rtokens=r[depcols[dty]]
			gsts+=rtokens
	return gsts

def get_term_tfidf_list(dtwl, tokenlist, d): ##returns a list, a la: [(<tfidf_score>, <term>), (0.00229568411387, 'nsubj$@%boy$@%play')]; ##this returned list represents terms that appear in the tokenlist and their tfidf scores based on the reference corpus ("doclist"). The tokenlist might be the GS, or it might be the test response; this will work on either.
	total_number_corpus_docs = len(dtwl)
	tfidf_scores_and_terms_pairlist = []
	typelist=[]
	for token in tokenlist:
		if token not in typelist:
			typelist.append(token)
		else: pass
	for wordtype in typelist:
		testdoc_term_raw_freq = tokenlist.count(wordtype)
		num_of_docs_with_term = 0
		for wl in dtwl:
			if wordtype in wl:
				num_of_docs_with_term += 1
			else: pass
		wordtype_tfidf = testdoc_term_raw_freq * (math.log(total_number_corpus_docs/(1.0 + num_of_docs_with_term)))
		tfidf_scores_and_terms_pairlist.append((wordtype_tfidf, wordtype))
	return tfidf_scores_and_terms_pairlist

def get_union_vector(x, y):
	myunion = []
	for i in x:
		myunion.append(i[1])
	for j in y:
		if j[1] not in myunion:
			myunion.append(j[1])
	myunion.sort()
	return myunion ###['det$@%x$@%man ', 'nsubj$@%x$@%shoot ', 'dobj$@%x$@%shoot ', ...]

def get_TC_score(gspairs, testpairs, termsvec): ##returns the TC score (tf-idf cosine) as described in King and Dickinson 2016
	gsdict={}
	testdict={}
	for gt in gspairs:
		gsdict[gt[1]]=gt[0]
	for tt in testpairs:
		testdict[tt[1]]=tt[0]
	gsvec=[]
	testvec=[]
	for term in termsvec:
		if term in gsdict:
			gsvec.append(gsdict[term])
		else:
			gsvec.append(0.0)
		if term in testdict:
			testvec.append(testdict[term])
		else:
			testvec.append(0.0)
	mycosine = cosine(testvec, gsvec)
	return mycosine

def write_output(rs, nm):
	thisfile=open(outputdir+nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()

def main():
	dtwdict=build_ref_wordlists() ##{'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}
	header, allinput=get_source_content(testdocfn)
	header=header+['ldh tfidf cosine', 'xdh tfidf cosine', 'xdx tfidf cosine']
	ldh_scores=[]
	xdh_scores=[]
	xdx_scores=[]
	ci=0 ##current index
	while ci < len(allinput):
		for deptype in ['ldh', 'xdh', 'xdx']:
			# print deptype
			# print '\n\n\n'
			currtestrow, currgsrows=get_current_split(allinput, ci)
			# print 'curr test row resp: '
			# print currtestrow[1]
			# print 'curr gs rows resps: '
			# for cg in currgsrows:
			# 	for c in cg:
			# 		print c[1]
			# 	print '\n'
			dtw=dtwdict[deptype] ##[[terms from doc 1], [terms from doc 2], etc.]
			mytesttokens = get_test_tokens(currtestrow, deptype)
			mygstokens = get_gs_tokens(currgsrows, deptype)
			gs_tfidf_pairs = get_term_tfidf_list(dtw, mygstokens, deptype)
			test_tfidf_pairs = get_term_tfidf_list(dtw, mytesttokens, deptype)
			terms_union_vector = get_union_vector(gs_tfidf_pairs, test_tfidf_pairs)
			test_TC_score = get_TC_score(gs_tfidf_pairs, test_tfidf_pairs, terms_union_vector) ##the "TC" Tf-idf Cosine score, as described in King & Dickinson 2016. We get the union set of terms for the test response and the GS, sort it, then create a vector of the GS scores for each term in the sorted union list, and a vector for the test scores for each term in the sorted union list; we calculate the cosine distance between these two vectors and use this as the TC score for the response.
			if deptype=='ldh':
				ldh_scores.append(test_TC_score)
			elif deptype=='xdh':
				xdh_scores.append(test_TC_score)
			elif deptype=='xdx':
				xdx_scores.append(test_TC_score)
			else:
				pass
		ci+=1
	ni=0
	outputrows=[]
	while ni<len(allinput):
		origrow=allinput[ni]
		origrow.append(ldh_scores[ni])
		origrow.append(xdh_scores[ni])
		origrow.append(xdx_scores[ni])
		outputrows.append(origrow)
		ni+=1
	outputrows.insert(0, header)
	outname=testdocfn[:-14] ##"I01T_all_cns_depstrings.csv" --> "I01T_all_cns_"
	outname=outname+'LOO_TC.csv' ##--> "I01T_all_cns_LOO_TC.csv" ##for Leave-One-Out Tf-idf Cosine
	write_output(outputrows, outname)

if __name__ == "__main__":
    main()

##I want this to flow like this:
#for item: ##this is handled in the bash shell, not in the python
	#for row:
		#for deptype:
		