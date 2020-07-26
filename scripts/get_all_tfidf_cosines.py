#!/usr/bin/env python


## 2020/07/25. This script finds all the test files in the test directory, then finds all the corresponding training files, then trains a model from each training file and uses these models to score all the test files; a scored version of each test file is written to a new file in the output directory. A separate file is written per model, per test_response, per dependency_format; this file contains the union vector of all terms in the model and test, along with the model tf-idf vector and test tf-idf vector (for those same terms). The vast majority won't be needed but these could help me explain trends later if I need to examine the processing closely.

import sys, math, csv
from os import walk
from scipy.spatial.distance import cosine


def get_refdoc_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir):
		docnames.extend(filenames)
		break
	return docnames


def get_terms_list(somedoc, d):
	terms = []
	with open(refcorpusdir+d+'/'+somedoc) as currdoc:
		for cline in currdoc:
			clist = cline.strip().split()
			clist = filter(None, clist)
			for t in clist:
				terms.append(t)
	return terms


def build_ref_termlists():
	dttermlists={}
	dts=['ldh', 'xdh', 'xdx']
	for dt in dts:
		myrefdocs = get_refdoc_names(refcorpusdir+dt) #reference corpus
		doctermlists=[]
		for refdoc in myrefdocs:
			reftokens = get_terms_list(refdoc, dt)
			doctermlists.append(reftokens)
		dttermlists[dt]=doctermlists
	return dttermlists ##{'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}


def get_test_file_names(t_dir):
	test_file_names = []
	for (dirpath, dirnames, filenames) in walk(t_dir):
		test_file_names.extend(filenames)
		break
	test_file_names = [dn for dn in test_file_names if ".csv" in dn]
	test_file_names.sort()
	return test_file_names


def get_training_file_names(inum, tr_dir): 
	training_file_names = []
	for (dirpath, dirnames, filenames) in walk(tr_dir):
		training_file_names.extend(filenames)
		break
	training_file_names = [dn for dn in training_file_names if inum in dn]
	training_file_names.sort()
	return training_file_names


def get_source_content(tdf): ## tdf ~= test doc file; returns csv lines as lists
	everything=[]
	tdoc=open(tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


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


## This simply pulls a list of all dependency tokens from the test response (in the relevant deptype (ldh, xdh, xdx))
def get_test_tokens(trow, dt):
	## trow type is list; looks like:
	"""['I01T-gNSF-p142-r1', 'The boy is dancing.', '1', '1', '1', '1', '1', '1\tthe\t_\tDT\tDT\t_\t2\tdet\t_\t_\n2\tboy\t_\tNN\tNN\t_\t4\tnsubj\t_\t_\n3\tbe\t_\tVBZ\tVBZ\t_\t4\taux\t_\t_\n4\tdance\t_\tVBG\tVBG\t_\t0\troot\t_\t_\n5\t.\t_\t.\t.\t_\t4\tpunct\t_\t_', "['det$@%the$@%boy', 'nsubj$@%boy$@%dance', 'aux$@%be$@%dance', 'root$@%dance$@%VROOT', 'punct$@%.$@%dance']", "['x$@%the$@%boy', 'x$@%boy$@%dance', 'x$@%be$@%dance', 'x$@%dance$@%VROOT', 'x$@%.$@%dance']", "['x$@%the$@%x', 'x$@%boy$@%x', 'x$@%be$@%x', 'x$@%dance$@%x', 'x$@%.$@%x']"]"""
	## So note how the fields of the CSV that contain the test tokens are stored as a string that looks like a python list -- ugh. The ugly processing here is to turn it into an actual list object...
	tts = string_list_to_real_list(trow, dt)
	# # print type(tts)
	## tts is now a list object of ldh|xdh|xdx like this: ['x$@%the$@%boy', 'x$@%boy$@%dance', 'x$@%be$@%dance', 'x$@%dance$@%VROOT', 'x$@%.$@%dance']
	return tts


def get_tokens(gsrows, dty):
	gsts=[]
	for gsrow in gsrows:
		rtokens = string_list_to_real_list(gsrow,dty)
		gsts.append(rtokens) ## List of lists; an inner list is all terms in a gs response
	return gsts


#test_tfidf_pairs = get_tfidf_pairs(dtw, [mytesttokens], deptype)
def get_tfidf_pairs(dtwl, listtokenlist, d): ##dtwl=[[terms from reference doc 1], [terms from ref doc 2], etc.]; listtokenlist=LIST OF LISTS of dependency tokens (from training response), so each inner list represents 1 (training) response; d=deptype ('ldh', etc.) ##returns a list, a la: [(<tfidf_score>, <term>), (0.00229568411387, 'nsubj$@%boy$@%play')]; ##this returned list represents terms that appear in the tokenlist and their tfidf scores based on the reference corpus ("doclist").
	tokenlist = [i for sublist in listtokenlist for i in sublist] ## flatten 2d list
	total_number_corpus_docs = len(dtwl)
	tfidf_scores_and_terms_pairlist = []
	typelist=[]
	for token in tokenlist:
		if token not in typelist:
			typelist.append(token)
		else: pass
	for termtype in typelist:
		testdoc_term_raw_freq = tokenlist.count(termtype)
		num_of_docs_with_term = 0
		for wl in dtwl:
			if termtype in wl:
				num_of_docs_with_term += 1
			else: pass
		termtype_tfidf = testdoc_term_raw_freq * (math.log(total_number_corpus_docs/(1.0 + num_of_docs_with_term)))
		tfidf_scores_and_terms_pairlist.append((termtype_tfidf, termtype))
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


def write_vectors_to_file(terms_union_v, modelv, testv, cos, vecs_path_nm):
	header = ["term", "model tf-idf", "test tf-idf", "(last cell in A is cos)"]
	vecfile=open(vecs_path_nm, 'w')
	vecwriter=csv.writer(vecfile, dialect=csv.excel)
	vecwriter.writerow(header)
	outrows = []
	vi = 0
	while vi < len(terms_union_v):
		virow = []
		virow.append(terms_union_v[vi])
		virow.append(modelv[vi])
		virow.append(testv[vi])
		outrows.append(virow)
		vi += 1
	for o in outrows:
		vecwriter.writerow(o)
	vecwriter.writerow([cos])


def get_TC_score(modelpairs, testpairs, terms_union_vec, vecs_path_name): ##returns the TC score (tf-idf cosine) as described in King and Dickinson 2016
	modeldict={}
	testdict={}
	for modelt in modelpairs:
		modeldict[modelt[1]]=modelt[0]
	for testt in testpairs:
		testdict[testt[1]]=testt[0]
	modelvec=[]
	testvec=[]
	for term in terms_union_vec:
		if term in modeldict:
			modelvec.append(modeldict[term])
		else:
			modelvec.append(0.0)
		if term in testdict:
			testvec.append(testdict[term])
		else:
			testvec.append(0.0)
	mycosine = cosine(testvec, modelvec)
	write_vectors_to_file(terms_union_vec, modelvec, testvec, mycosine, vecs_path_name)
	return mycosine


def write_output(rs, nm):
	outdir =('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/N70/')
	thisfile=open(outdir+nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


testdir=('/Users/leviking/Documents/dissertation/SAILS/test_data/N70/')
trainingdir=('/Users/leviking/Documents/dissertation/SAILS/training_data/N50/')
scored_vecs_dir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/N70/')
refcorpusdir=('/Users/leviking/Documents/dissertation/SAILS_annex/brown/')
depcols={'ldh':8, 'xdh':9, 'xdx':10} ##the columns where each deptype is stored in the input files


def main():
	test_file_names = get_test_file_names(testdir)
	dtwdict = build_ref_termlists() ##This contains everything from the reference corpus. {'ldh': [[terms from doc 1], [terms from doc 2], etc.], 'xdh': [[terms], [terms]], etc.}
	for testfn in test_file_names:
		print("\nCurrent test: "+testfn)
		itemnum = testfn.split("-")[0]  ## e.g., I01T
		training_fns = get_training_file_names(itemnum, trainingdir)
		header, all_test_rows=get_source_content(testdir+testfn) ## This is one CSV; header is row, all_test_rows is list of rows
		header=header+['ldh TC', 'xdh TC', 'xdx TC']
		for trainingfn in training_fns:
			print("\tCurrent model: "+trainingfn)
			dummy, curr_training_rows = get_source_content(trainingdir+trainingfn)
			ldh_scores=[]
			xdh_scores=[]
			xdx_scores=[]
			for deptype in ['ldh', 'xdh', 'xdx']:
				training_label = trainingfn.replace(".csv", "-"+deptype)
				dtw=dtwdict[deptype] ##[[terms from doc 1], [terms from doc 2], etc.] ##NOTE: len(dtw) is 483 in all cases (483 documents)
				training_tokens = get_tokens(curr_training_rows, deptype) ## training_tokens is list of lists of depstrings
				model_tfidf_pairs = get_tfidf_pairs(dtw, training_tokens, deptype)
				for test_row in all_test_rows:
					participant_id = test_row[0][10:14]  ## "I01U-gNNS-p004-r1" --> "p004" (the participant ID is the only relevant part of the response ID at this stage)
					vectors_path_name = scored_vecs_dir+"term_vectors/"+training_label+"-VS-"+participant_id+".csv"
					mytesttokens = get_test_tokens(test_row, deptype) ## mytesttokens is list of terms (depstrings) in test response
			# test_w_tfidf_pairs = get_weighted_term_tfidf_list(dtw, [mytesttokens], deptype) #### REVISIT this! ##hacky solution -- list containing only one sublist
			# terms_w_union_vector = get_union_vector(gs_w_tfidf_pairs, test_w_tfidf_pairs)
			# test_w_TC_score = get_TC_score(gs_w_tfidf_pairs, test_w_tfidf_pairs, terms_w_union_vector) ##the "TC" Tf-idf Cosine score, as described in King & Dickinson 2016. We get the union set of terms for the test response and the GS, sort it, then create a vector of the GS scores for each term in the sorted union list, and a vector for the test scores for each term in the sorted union list; we calculate the cosine distance between these two vectors and use this as the TC score for the response.
					test_tfidf_pairs = get_tfidf_pairs(dtw, [mytesttokens], deptype)
					terms_union_vector = get_union_vector(model_tfidf_pairs, test_tfidf_pairs)
					test_TC_score = get_TC_score(model_tfidf_pairs, test_tfidf_pairs, terms_union_vector, vectors_path_name)
					if deptype=='ldh':
						ldh_scores.append(test_TC_score)
					elif deptype=='xdh':
						xdh_scores.append(test_TC_score)
					elif deptype=='xdx':
						xdx_scores.append(test_TC_score)
					else:
						pass
			ni=0
			outputrows=[header]
			while ni<len(all_test_rows):
				origrow=all_test_rows[ni]
				origrow.append(ldh_scores[ni])
				origrow.append(xdh_scores[ni])
				origrow.append(xdx_scores[ni])
				outputrows.append(origrow)
				ni+=1
			outname=trainingfn.replace(".csv", "-VS-N70.csv")
			write_output(outputrows, outname)


if __name__ == "__main__":
    main()

