#!/usr/bin/env python

##2019-06-22. This is a modified version of lk_tfidf_LOO_TC_weighted.py.

##2018-08-14. LK. This script takes an output file from prep_conll_for_tfidf.py / prep_conll_for_tfidf.sh. So far, those output files have been like this: each one represents all NNS responses for a particular item (e.g., item 1 untargeted, or item 19 targeted). Each file is a csv, where the columns are like so (this is the header):
##ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx
##(obvious)		(These five are annotation: "1" or "0")				(lemmatized CoNNL parse (multiline cell))	(ldh, etc. are "depstrings"--each dependency is a concatenated string with a delimiter symbol)
##
##This relies on a reference corpus; here, I use the Brown corpus, and the documents in the corpus have been prepared as depstrings; there are separate versions for ldh, xdh and xdx.
##
##For each of the 60 response items, this script finds the corresponding set of GSs. For each GS, it generates a set of weighted and unweighted tf-idf scores for each of the terms that appear in the GS, via the reference corpus. Then it iterates over each of the NNS responses and scores and produces a set of weighted and unweighted scores for each of the terms in the NNS response.
##It scores each response using the "TC" tf-idf cosine method described in King and Dickinson 2016. TC takes the GS and gives each term (depstring) a tf-idf score via the reference corpus. Then it does the same for the test response. It creates a union list of the terms in the GS and the test response, sorts it, then creates a corresponding GS vector with the GS tf-idf scores, and a test vector with the corresponding test tf-idf scores. It then calculates the cosine of these two vectors, resulting in a single score for the test response, which represents the test response distance from the GS.

## for item:
	## initialize TC score list for each depstring format
	## get all GSs
	## for GS:
		## get weighted tf-idf vector; cache it
		## get unweighted tf-idf vector; cache it
		## for response:
			## for depstring format:
				## get weighted tf-idf vector; cache it
				## get unweighted tf-idf vector; cache it
				## get TC score against GS vector; cache it; add to list for csv
	## write TC scores to csv
			

##### BELOW: Not verified since updated (2019/06/22)
##The output is a csv, where the first 11 columns are identical to the input csv, and the next three columns are the TC score for ldh, xdh and xdx depstrings. This file is the same filename as the input, with "depstrings.csv" replaced with "LOO_TC.csv"; the output file is stored in a sister folder to the input file folder, called "LOO_TC".
##
##USAGE:
##python lk_tfidf_LOO_TC_weighted.py inputfile ###inputfile is e.g., "../gold_standards/depstrings/I01T_all_fns_depstrings.csv"
##
##This script is intended to be run via the lk_tfidf_TC.sh shell, which will iterate through all files in the "depstrings" folder.
##### ABOVE: Not verified since updated (2019/06/22)

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
outputdir=('/Users/leviking/Documents/dissertation/SAILS/responses/TC/')
depcols={'ldh':8, 'xdh':9, 'xdx':10} ##the columns where each deptype is stored

def get_refdoc_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	return docnames

def get_word_list(somedoc, d):
## Note that "words" here is really depstrings: 'nsubj$@%man$@%find', 'x$@%man$@%find', etc.
## The corpus docs are already stored as such
	wds = []
	with open(mycorpusdir+d+'/'+somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for w in clist:
				wds.append(w)
	return wds

def build_ref_wordlists():
## Again, "words" here are depstrings
	dtwordlists={}
	dts=['ldh', 'xdh', 'xdx']
	for dt in dts:
		myrefdocs = get_refdoc_names(mycorpusdir+dt) ##this is the reference corpus
		docwordlists=[]
		for refdoc in myrefdocs:
			reftokens = get_word_list(refdoc, dt)
			docwordlists.append(reftokens)
		dtwordlists[dt]=docwordlists
	return dtwordlists ##{'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}

def get_source_content(tdf): ## tdf ~= test doc file; returns csv lines as lists
	everything=[]
	tdoc=open(sourcedir+tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything

##changed this slightly from the unweighted version of the script;
## this does the LOO split -- 1 response from GS pool becomes test response, the rest are used as GS
## Note, returned test item is one list of dependencies; returned GS is list of lists of dependencies
# # def get_current_split(allinput, c):
# # 	cgsrows=[]
# # 	ctestrow=allinput[c]
# # 	for r in allinput[:c]:
# # 		cgsrows.append(r)
# # 	for r in allinput[int(c)+1:]:
# # 		cgsrows.append(r)
# # 	return ctestrow, cgsrows

## uglyrow here is a csv row; it's a list, but some columns contain python lists STORED AS QUOTED STRINGS! e.g, the "trow" argument of get_test_tokens is an uglyrow. 
def string_list_to_real_list(uglyrow, dtype):
	pylist = uglyrow[depcols[dtype]]
	pylist = pylist[1:-1] ## remove the list brackets; still a string
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%") ##temporarily replace real text commas so we can split on the list commas
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist

## This simply pulls a list of all depdency tokens from the test response (in the relevant deptype (ldh, xdh, xdx))
def get_test_tokens(trow, dt):
	## trow type is list; looks like:
	"""['I01T-gNSF-p142-r1', 'The boy is dancing.', '1', '1', '1', '1', '1', '1\tthe\t_\tDT\tDT\t_\t2\tdet\t_\t_\n2\tboy\t_\tNN\tNN\t_\t4\tnsubj\t_\t_\n3\tbe\t_\tVBZ\tVBZ\t_\t4\taux\t_\t_\n4\tdance\t_\tVBG\tVBG\t_\t0\troot\t_\t_\n5\t.\t_\t.\t.\t_\t4\tpunct\t_\t_', "['det$@%the$@%boy', 'nsubj$@%boy$@%dance', 'aux$@%be$@%dance', 'root$@%dance$@%VROOT', 'punct$@%.$@%dance']", "['x$@%the$@%boy', 'x$@%boy$@%dance', 'x$@%be$@%dance', 'x$@%dance$@%VROOT', 'x$@%.$@%dance']", "['x$@%the$@%x', 'x$@%boy$@%x', 'x$@%be$@%x', 'x$@%dance$@%x', 'x$@%.$@%x']"]"""
	## So note how the fields of the CSV that contain the test tokens are stored as a string that looks like a python list -- ugh. The ugly processing here is to turn it into an actual list object...
	tts = string_list_to_real_list(trow, dt)
	# # print type(tts)
	## tts is now a list object of ldh|xdh|xdx like this: ['x$@%the$@%boy', 'x$@%boy$@%dance', 'x$@%be$@%dance', 'x$@%dance$@%VROOT', 'x$@%.$@%dance']
	return tts

def get_gs_tokens(gsrows, dty):
	gsts=[]
	for gsrow in gsrows:
		rtokens = string_list_to_real_list(gsrow,dty)
		gsts.append(rtokens) ## List of lists; an inner list is all terms in a gs response; this nested structure (not flat) is necessary for weighting
	return gsts

## 2019-05-11. OK, weighting has been implemented.
def get_weighted_term_tfidf_list(dtwl, listtokenlist, d): ##dtwl=[[terms from doc 1], [terms from doc 2], etc.]; tokenlist=LIST OF LISTS of dependency tokens (from GS response), so each inner list represents 1 (GS) response; d=deptype ('ldh', etc.) ##returns a list, a la: [(<tfidf_score>, <term>), (0.00229568411387, 'nsubj$@%boy$@%play')]; ##this returned list represents terms that appear in the tokenlist and their tfidf scores based on the reference corpus ("doclist").
	total_number_corpus_docs = float(len(dtwl))
	tfidf_scores_and_terms_pairlist = []	
	allresptypelist=[]
	allresptypedict={}
	for tokenlist in listtokenlist:
		for token in tokenlist:
			if token not in allresptypedict:
				allresptypedict[token] = float(tokenlist.count(token)/float(len(tokenlist)))
				allresptypelist.append(token)
			else:
				allresptypedict[token] += float(tokenlist.count(token)/float(len(tokenlist)))
## from here, the weights should already be attached to the wordtypes; we need to check a dict for the weight				
	for wordtype in allresptypelist:
		testdoc_term_weighted_freq = allresptypedict[wordtype]
		num_of_docs_with_term = 0.0
		for wl in dtwl:
			if wordtype in wl:
				num_of_docs_with_term += 1.0
			else: pass
		wordtype_tfidf = testdoc_term_weighted_freq * (math.log(total_number_corpus_docs/(1.0 + num_of_docs_with_term)))
		tfidf_scores_and_terms_pairlist.append((wordtype_tfidf, wordtype))
	return tfidf_scores_and_terms_pairlist

def get_unweighted_term_tfidf_list(dtwl, listtokenlist, d):  ## same inputs as weighted function
	tokenlist = [i for sublist in listtokenlist for i in sublist] ## flatten 2d list; we don't need 2d for unweighted
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

# for item (this iteration handled in shell):
	## (This python script starts with next line)
	## initialize TC score list for each depstring format
	## get all GSs
	## for GS:
		## get weighted tf-idf vector; cache it
		## get unweighted tf-idf vector; cache it
		## for response:
			## for depstring format:
				## get weighted tf-idf vector; cache it
				## get unweighted tf-idf vector; cache it
				## get TC score against GS vector; cache it; add to list for csv
	## write TC scores to csv

def prep_all_gs_material():
	pass

def main():
	dtwdict=build_ref_wordlists() ##This contains everything from the reference corpus. {'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}
	header, all_test_rows=get_source_content(testdocfn) ## This is one CSV; header is row, all_test_rows is list of rows
	header=header+['ldh TC weighted', 'xdh TC weighted', 'xdx TC weighted', 'ldh TC unweighted', 'xdh TC unweighted', 'xdx TC unweighted'] ## We're adding these columns for scoring
	ldh_w_scores=[]
	xdh_w_scores=[]
	xdx_w_scores=[]
	ldh_uw_scores=[]
	xdh_uw_scores=[]
	xdx_uw_scores=[]
	
	### 2019/06/26. Clean up in and around here; I believe we want to first gather all the GSs and their materials; then we want to iterate through the test rows...
	
	for test_row in all_test_rows:
		pass

	for deptype in ['ldh', 'xdh', 'xdx']:
		#### Below: universal / shared for weighted & unweighted ####
		dtw=dtwdict[deptype] ##[[terms from doc 1], [terms from doc 2], etc.] ##NOTE: len(dtw) is 483 in all cases (483 documents)
		mytesttokens = get_test_tokens(test_row, deptype) ## mytesttokens is list of terms (depstrings) in test response
		mygstokens = get_gs_tokens(currgsrows, deptype) ## mygstokens is list of lists of depstrings
		#### Above: universal / shared for weighted & unweighted ####
		gs_w_tfidf_pairs = get_weighted_term_tfidf_list(dtw, mygstokens, deptype)
		test_w_tfidf_pairs = get_weighted_term_tfidf_list(dtw, [mytesttokens], deptype) #### REVISIT this! ##hacky solution -- list containing only one sublist
		terms_w_union_vector = get_union_vector(gs_w_tfidf_pairs, test_w_tfidf_pairs)
		test_w_TC_score = get_TC_score(gs_w_tfidf_pairs, test_w_tfidf_pairs, terms_w_union_vector) ##the "TC" Tf-idf Cosine score, as described in King & Dickinson 2016. We get the union set of terms for the test response and the GS, sort it, then create a vector of the GS scores for each term in the sorted union list, and a vector for the test scores for each term in the sorted union list; we calculate the cosine distance between these two vectors and use this as the TC score for the response.
		gs_uw_tfidf_pairs = get_unweighted_term_tfidf_list(dtw, mygstokens, deptype)
		test_uw_tfidf_pairs = get_unweighted_term_tfidf_list(dtw, [mytesttokens], deptype) #### REVISIT this! ##hacky solution -- list containing only one sublist
		terms_uw_union_vector = get_union_vector(gs_uw_tfidf_pairs, test_uw_tfidf_pairs)
		test_uw_TC_score = get_TC_score(gs_uw_tfidf_pairs, test_uw_tfidf_pairs, terms_uw_union_vector)
		if deptype=='ldh':
			ldh_w_scores.append(test_w_TC_score)
			ldh_uw_scores.append(test_uw_TC_score)
		elif deptype=='xdh':
			xdh_w_scores.append(test_w_TC_score)
			xdh_uw_scores.append(test_uw_TC_score)
		elif deptype=='xdx':
			xdx_w_scores.append(test_w_TC_score)
			xdx_uw_scores.append(test_uw_TC_score)
		else:
			pass
		# # ci+=1
	ni=0
	outputrows=[]
	while ni<len(all_test_rows):
		origrow=all_test_rows[ni]
		###	header=header+['ldh TC weighted', 'xdh TC weighted', 'xdx TC weighted', 'ldh TC unweighted', 'xdh TC unweighted', 'xdx TC unweighted'] ## We're adding these columns for scoring
		origrow.append(ldh_w_scores[ni])
		origrow.append(xdh_w_scores[ni])
		origrow.append(xdx_w_scores[ni])
		origrow.append(ldh_uw_scores[ni])
		origrow.append(xdh_uw_scores[ni])
		origrow.append(xdx_uw_scores[ni])
		outputrows.append(origrow)
		ni+=1
	outputrows.insert(0, header)
	outname=testdocfn[:-14] ##"I01T_all_cns_depstrings.csv" --> "I01T_all_cns_"
	outname=outname+'LOO_TC-w.csv' ##--> "I01T_all_cns_LOO_TC-w.csv" ##for Leave-One-Out Tf-idf Cosine; "w" for weighted.
	write_output(outputrows, outname)

if __name__ == "__main__":
    main()

		