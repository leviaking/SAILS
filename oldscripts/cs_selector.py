#!/usr/bin/env python

###2013/11/26. This script is intended to parse the output of the CMU SLM Toolkit evallm module. Specifically, I use another script to process a NNS sentence response to a PDT, and using NS responses and a spelling correction/suggestion module (Aspell/Enchant), I produce a list of candidate sentences for that NNS sentence (this is based on the assumption that words in the NNS sentence may have been incorrectly spelled). The candidates are then passed through the language model evaluator, producing output of the form seen below. This script needs to perform two major tasks: 1) exclude any sentences containing OOVs, 2) select the remaining sentence with the lowest perplexity score.
#
##usage: python cs_selector.py item01

import os, shutil, sys
item=sys.argv[1]
itemnum=item.strip().split('item')[-1]
#print itemnum

###Put this part at the beginning!###
def get_file_lists():
	## this returns a list of all the ".perplexity" files for ALL NNS input sentence for a single PDT item, and a list of the NNS sentences' numbers.
	walker = os.walk('../data/candidate_sentences/'+item+'/')
	for x, y, z in walker:
		messy_list = z
	all_inputs=[] ## This becomes the list of all candidate sentences for one item; e.g., for item01, it's all candidates for *all* NNS input sentences.
	for b in messy_list:
		if b.startswith('.'): pass
		elif b.endswith('perplexity'): all_inputs.append(b)
		else: pass
	#print all_inputs
	nns_sents=[] ## This becomes the list of all the NNS input sentence numbers; for now (9/12/2014), this is always 001-039.
	for b in all_inputs:
		nns_sent_num=b[3:6]
		if nns_sent_num not in nns_sents:
			nns_sents.append(nns_sent_num)
		else: pass
	#print nns_sents
	return all_inputs, nns_sents

def get_eop(curr_NNS):
	## this returns a string object containing the text of all the individual evallm output files for the candidate sentences for a SINGLE NNS input sentence for the current item.
	curr_candidates=[]
	for input_x in all_inputs:
		x_num = input_x[3:6]
		if x_num == curr_NNS_num:
			curr_candidates.append(input_x)
		else: pass
	curr_eop='' ## "eop" is for "evallm output"
	### Re: this "curr_tail" business... For whatever reason, evallm doubles the output for the final candidate sentence, and this bit of code fixes this so we only have one copy.
	curr_candidates.sort()
	curr_tail_name=curr_candidates.pop()
	curr_tail_file=open(''.join(['../data/candidate_sentences/', item, '/', curr_tail_name]), 'r')
	curr_tail_list=curr_tail_file.readlines()
	curr_tail_file.close()
	curr_tail=''.join([curr_tail_list[0], curr_tail_list[1], curr_tail_list[2], curr_tail_list[3], curr_tail_list[4], curr_tail_list[5], curr_tail_list[6], curr_tail_list[7]])
	###
	for curr_x in curr_candidates:
		infile = open(''.join(['../data/candidate_sentences/', item, '/', curr_x]), 'r')
		eop_x=infile.read().strip()+'\n' ## "eop" is for "evallm output"
		infile.close()
		curr_eop=curr_eop+eop_x
	curr_eop=curr_eop+curr_tail
	return curr_eop


###########input01='''Computing perplexity of the language model with respect
###########   to the text ../../candidate_sentences/item01/01_001_0008.txt
###########Perplexity = 1290.44, Entropy = 10.33 bits
###########Computation based on 8 words.
###########Number of 3-grams hit = 3  (37.50%)
###########Number of 2-grams hit = 2  (25.00%)
###########Number of 1-grams hit = 3  (37.50%)
###########0 OOVs (0.00%) and 0 context cues were removed from the calculation.'''
###########
###########input02='''Computing perplexity of the language model with respect
###########   to the text ../../candidate_sentences/item01/01_001_0009.txt
###########Perplexity = 869.09, Entropy = 9.76 bits
###########Computation based on 8 words.
###########Number of 3-grams hit = 3  (37.50%)
###########Number of 2-grams hit = 3  (37.50%)
###########Number of 1-grams hit = 2  (25.00%)
###########0 OOVs (0.00%) and 0 context cues were removed from the calculation.'''
###########
###########input03='''Computing perplexity of the language model with respect
###########   to the text ../../candidate_sentences/item01/01_001_0010.txt
###########Perplexity = 190.93, Entropy = 7.58 bits
###########Computation based on 7 words.
###########Number of 3-grams hit = 5  (71.43%)
###########Number of 2-grams hit = 1  (14.29%)
###########Number of 1-grams hit = 1  (14.29%)
###########1 OOVs (12.50%) and 0 context cues were removed from the calculation.
###########Computing perplexity of the language model with respect
###########   to the text ../../candidate_sentences/item01/01_001_0010.txt
###########Perplexity = 190.93, Entropy = 7.58 bits
###########Computation based on 7 words.
###########Number of 3-grams hit = 5  (71.43%)
###########Number of 2-grams hit = 1  (14.29%)
###########Number of 1-grams hit = 1  (14.29%)
###########1 OOVs (12.50%) and 0 context cues were removed from the calculation.'''
###########
###########all_inputs=[input01, input02, input03]
#


def get_eopd(eop):
	##get a dictionary; eopd = {filename: perplexity}
	eopd = {}
	eopl = eop.split('calculation.\n')
	eopl=filter(None, eopl)
	for i in eopl:
		il = filter(None, i.split('Computing perplexity of the language model with respect\n   to the text '))
		istr = il[0]
		#print istr
	###'../../../data/candidate_sentences/item01/01_008_0165.txt\nPerplexity = 686.75, Entropy = 9.42 bits\nComputation based on 4 words.\nNumber of 3-grams hit = 1  (25.00%)\nNumber of 2-grams hit = 2  (50.00%)\nNumber of 1-grams hit = 1  (25.00%)\n1 OOVs (20.00%) and 0 context cues were removed from the calculation.'
		il = filter(None, istr.split('\nPerplexity = '))
		#print il
		cs = il.pop(0) #candidate sentence; the path and filename
		#print "CS: ", cs
		#print cs.split('../../candidate_sentences/item01/')
		cs = cs.split('../../../data/candidate_sentences/'+item+'/')[1] #now cs is only the filename-- we don't want the path now
		istr = il.pop(0)
		#print cs, ': ', istr
		il = filter(None, istr.split(', Entropy = '))
		perplexity = float(il.pop(0)) ##convert string numeral to float numeral-- very important for sorting!
		istr = il.pop(0)
		#print perplexity, ': ', istr
		il = filter(None, istr.split('\n'))
		#print len(il)
		oovi = il[5]
		if oovi.startswith('0 OOVs'):
			eopd[cs] = perplexity
		else: pass
	#for cs in eopd:
	#	print cs, ': ', eopd[cs]
	#print len(eopd)
	return eopd

def select_sentences(eopd):
	##choose the sentence with the lowest perplexity. this needs to consider the possibility of a tie. if there is a tie, and the original sentence is in the tie, choose the original sentence. otherwise...?
	psl = [] ##perplexity score list
	for cs in eopd:
		psl.append(eopd[cs])
	psl.sort()
	#print psl
	#print eopd, '\n\n\n'
	lowperplex = psl[0] ##this is the lowest perplexity score; note that it could occur more than once (candidate sentences can be tied for lowest perplexity)
	lowcs = [] ##this list will contain the filename(s) of the cs with lowest perplexity; if no tie, it will contain only 1 item
	for cs in eopd:
		if eopd[cs] == lowperplex:
			lowcs.append(cs)
		else: pass ##do nothing
	###the following commented lines would be used if we wanted to (somewhat arbitrarily) choose a single sentence in the case of a tie. 
	#if len(lowcs) > 1: ## if there's a tie; in this case, check for the original sentence and select it if present; if original not present, take the first cs. in fact, we can always simply take the first item after sorting lowcs, because the original sentence always has the lowest numbered filename.
	#	lowcs.sort()
	#	#print lowcs
	#	winner = lowcs[0]
	#else: winner = lowcs[0]
	#return winner
	return lowcs
#		
#
###main program
all_inputs, nns_sents = get_file_lists()
for curr_NNS_num in nns_sents:
	curr_eop = get_eop(curr_NNS_num)
	#print curr_eop
	#print '\n\n\n'
	#print curr_candidates
	eopd=get_eopd(curr_eop) ## "eopd" is for "evallm output dictionary"
	print eopd, '\n\n\n\n\n\n\n'
	lowcs = select_sentences(eopd)
	lowcs.sort()
	#print lowcs, '\n'
	outfilename=''.join([itemnum, '_', curr_NNS_num, '_best.txt'])
	outfile = open(''.join(['../data/best_sentence_lists/', item, '/', outfilename]), 'w')
	for s in lowcs:
		outfile.write(s)
		outfile.write('\n')
	outfile.close()

##### 2014/09/03. LK: In theory, there could be ties for perplexity. In actuality, I've only seen ties between candidates 0000 and 0001; like this, where this is the content of a "best sentence lists" file (01_001_best.txt):
##### 01_001_0000.txt
##### 01_001_0001.txt
##### In cases like this, candidates 0000 and 0001 are ALWAYS identical/duplicate sentences. This next bit of code was added to find such cases and remove the 0001 listing from the best sentences list file.
best_walker=os.walk('../data/best_sentence_lists/'+item+'/')
for u, v, w in best_walker:
	besties=w
	#print besties
for bslfilename in besties:
	if bslfilename.startswith('.'):
		pass
	else:
		with open(''.join(['../data/best_sentence_lists/', item, '/', bslfilename]), 'r+') as myfile:
			intext=myfile.read().strip()
			inlines=intext.split('\n')
			#print inlines
			inlines=filter(None, inlines)
			#print "number of lines: ", len(inlines)
			if len(inlines) == 1:
				myfile.close()
			elif len(inlines) > 1:
				keeper=inlines[0]
				myfile.seek(0) ## move write cursor to beginning of file
				myfile.truncate() ## remove file contents after cursor (here, this means all contents)
				myfile.write(keeper)
				myfile.close()
			else:
				myfile.close()
####
##### 2014/09/03. LK: now I want to add some code to make the subsequent steps in the pipeline easier. After running this script, I want to have a copy of each best sentence (not the filename, the actual file with the sentence) in "best_sentences/singles/", as well as a single file containing each sentence (IN THE CORRECT ORDER), in "best_sentences/".
allbests=open('../data/best_sentences/'+item+'/'+item+'_all_bests.txt', 'w')
final_walker=os.walk('../data/best_sentence_lists/'+item+'/')
for r, s, t in final_walker:
	b=t
for bname in b:
	if bname.startswith('.'):
		pass
	else:
		#print 'bname: ', bname
		shutil.copy2(''.join(['../data/best_sentence_lists/', item, '/', bname]), ''.join(['../data/best_sentences/', item, '/singles/', bname]))
		bi=open(''.join(['../data/best_sentence_lists/', item, '/', bname]), 'r')
		bindex=bi.read().strip()
		#print "bindex: ", bindex
		bi.close()
		bloc=''.join(['../data/best_sentence_lists/', item, '/', bname])
		#print 'bloc: ', bloc
		bfi=open(bloc, 'r')
		bcand=bfi.read().strip()
		#print 'bcand: ', bcand
		bfi.close()
		bcandfi=open('../data/candidate_sentences/'+item+'/'+bcand)
		btext=bcandfi.read().strip()
		bcandfi.close()
		allbests.write(''.join([btext, '\n']))
allbests.close()
