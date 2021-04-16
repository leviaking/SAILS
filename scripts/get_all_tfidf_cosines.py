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


def get_source_content(tdf):
	everything=[]
	tdoc=open(tdf, 'r')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def string_list_to_real_list(uglyrow, dtype):
	pylist = uglyrow[depcols[dtype]]
	pylist = pylist[1:-1]
	pylist = pylist.replace("$@%,$@%", "$@%COMMA$@%")
	pylist = pylist.split(",")
	pylist = [t for t in pylist if t]
	pylist = [t.replace("$@%COMMA$@%", "$@%,$@%") for t in pylist]
	pylist = [t.strip() for t in pylist]
	pylist = [t[1:-1] for t in pylist]
	return pylist


def get_test_tokens(trow, dt):
	tts = string_list_to_real_list(trow, dt)
	return tts


def get_tokens(gsrows, dty):
	gsts=[]
	for gsrow in gsrows:
		rtokens = string_list_to_real_list(gsrow,dty)
		gsts.append(rtokens)
	return gsts


def get_tfidf_pairs(dtwl, listtokenlist, d):
	tokenlist = [i for sublist in listtokenlist for i in sublist] ## flatten
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
	return myunion


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


def get_TC_score(modelpairs, testpairs, terms_union_vec, vecs_path_name):
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


def write_output(sname, rs, nm):
	outdir =('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'
			 +sname+'-VS-N70/')
	thisfile=open(outdir+nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


samplename = "N50"
testdir=('/Users/leviking/Documents/dissertation/SAILS/test_data/N70/')
trainingdir=('/Users/leviking/Documents/dissertation/SAILS/training_data/'
			 +samplename+"/")
scored_vecs_dir=('/Users/leviking/Documents/dissertation/SAILS/test_data/scored/'
				 +samplename+'-VS-N70/')
refcorpusdir=('/Users/leviking/Documents/dissertation/SAILS_annex/brown/')
depcols={'ldh':8, 'xdh':9, 'xdx':10}


def main():
	test_file_names = get_test_file_names(testdir)  ## e.g., I01T-NNS-test-N70.csv
	dtwdict = build_ref_termlists()
	for testfn in test_file_names:
		print("\nCurrent test: "+testfn)
		itemnum = testfn.split("-")[0]  ## e.g., I01T
		training_fns = get_training_file_names(itemnum, trainingdir)
		for trainingfn in training_fns:
			header, curr_test_rows=get_source_content(testdir+testfn) 
			header=header+['ldh TC', 'xdh TC', 'xdx TC']
			print("\tCurrent training: "+trainingfn)
			dummy, curr_training_rows = get_source_content(trainingdir+trainingfn)
			ldh_scores=[]
			xdh_scores=[]
			xdx_scores=[]
			for deptype in ['ldh', 'xdh', 'xdx']:
				training_label = trainingfn.replace(".csv", "-"+deptype)
				dtw=dtwdict[deptype]
				training_tokens = get_tokens(curr_training_rows, deptype)
				model_tfidf_pairs = get_tfidf_pairs(dtw, training_tokens, deptype)
				for test_row in curr_test_rows:
					participant_id = test_row[0][10:14]
					vectors_path_name = scored_vecs_dir+"term_vectors/"+training_label+"-VS-"+participant_id+".csv"
					mytesttokens = get_test_tokens(test_row, deptype)
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
			while ni<len(curr_test_rows):
				origrow=curr_test_rows[ni]
				origrow.append(ldh_scores[ni])
				origrow.append(xdh_scores[ni])
				origrow.append(xdx_scores[ni])
				outputrows.append(origrow)
				ni+=1
			outname=trainingfn.replace(".csv", "-VS-N70.csv")
			write_output(samplename, outputrows, outname)


if __name__ == "__main__":
    main()

