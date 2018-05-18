#!/usr/bin/env python

##2014/09/17. RENAMED from "LM_spelling_pipeline.py" to "get_spelling.py"!

##2013/11/30. At this point, this script takes hardcoded input: the list of NS sentences; the list of NNS sentences. For each NNS sentence, it generates candidate sentences-- each candidate sentence is numbered and written to a unique text file with that number as a filename (in "candidate_sentences/"), and a list of each candidate sentence filename is written to a file (in cs_indices); this output takes this form because the LM evaluation tool (evallm) takes a list of filenames and produces a perplexity score for each of those files.

##2014/09/04. LK: I've added a command line argument to indicate the item number ('item01', 'item02', etc.); this will be used to define the path for output. SO...
## USAGE: python LM_spelling_pipeline.py item01

## "##??" indicates an unresolved question in the code...

##?? (2013/12/1) Sometimes candidate sentences ...0000 and ...0001 are identical, but sometimes they are not. I'm not sure this is a big deal or if it can be easily fixed, but right now I'm not worrying about it... Not sure why it's happening...

#>>> import enchant
#>>> d = enchant.Dict('en')
#>>> d.check('shoot')
#True
#>>> d.suggest('shoot')
#['shoot', 'shot', 'Short', 'shoat', 'short', 'shout', 'shit', 'shoots', 'shooter', 'shirt', 'shoo', 'shooed', 'shorty', 'hoot', 'soot', 'shod', 'shut', 'shook', 'shoos', 'sheet', "shoot's"]

import nltk, pickle, enchant, re, sys
from nltk.tokenize import word_tokenize
from nltk.probability import LidstoneProbDist
from nltk.corpus import brown

item=sys.argv[1]
d = enchant.Dict('en')
##d.suggest('shoot')

##stopwords list; manually paste the top [100? 200?] words here as list object "stopwords".
stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
#
NNSraw_filename=''.join(['../data/originals/', item, '_originals.txt'])
NNSraw_file=open(NNSraw_filename, 'r')
NNSraw_text=NNSraw_file.read().strip()
NNSraw_file.close()
NNSraw=NNSraw_text.split('\n')
NNSraw=filter(None, NNSraw)
#
NSraw_filename=''.join(['../data/NS/', item, '_NS.txt'])
NSraw_file=open(NSraw_filename, 'r')
NSraw_text=NSraw_file.read().strip()
NSraw_file.close()
NSraw=NSraw_text.split('\n')
NSraw=filter(None, NSraw)

##Do we need to keep the NS bag and the stop words bag separate at any point? YES.
##Now we need a bag of words from the NS sentences:
def get_bag(sentlist):
	bag = []
	for sentence in sentlist:
		sentence = sentence.lower()
		sl = word_tokenize(sentence)
		for w in sl:
			if re.search('[a-zA-Z]', w):
				if w not in stopwords and w not in bag:
					##we check against the stopwords to avoid adding stopwords to the NS bag;
					bag.append(w)
				else: pass
			else: pass
	return bag

def make_package(rawsentence):
	##this function returns a dictionary which will be the main data structure for a NS sentence as it is processed through the rest of the pipeline. from a sentence: "A hunter shouted 2 birds, but 1 didn't die." we get: {0: ['UNFIXED', 'A'], 1: ['UNFIXED', 'hunter'], 2: ['UNFIXED', 'shouted'], 3: ['FIXED', '2'], 4: ['UNFIXED', 'birds'], 5: ['FIXED', ','], 6: ['UNFIXED', 'but'], 7: ['FIXED', '1'], 8: ['UNFIXED', 'did'], 9: ['UNFIXED', "n't"], 10: ['UNFIXED', 'die'], 11: ['FIXED', '.']}
	package = {}
	counter = 0
	rawsentence = rawsentence.lower()
	words = word_tokenize(rawsentence)
	for w in words:
		if not re.search('[a-zA-Z]', w):
			##this means that punctuation and numerals are FIXED; note that punctuation embedded in a word ("didn't") will NOT be FIXED
			package[counter] = ['FIXED', w]
		else:
			package[counter] = ['UNFIXED', w]
		counter+=1
	return package

def package_vs_stopwords(package):
	##this filters out stopwords; package words that are stop words become FIXED.
	for key in package:
		code = package[key][0]
		if code == 'UNFIXED':
			w = package[key][1]
			if w in stopwords:
				package[key] = ['FIXED', w]
			else: pass
		else: pass
	return package

def package_vs_NSbag(package):
	##this filters out NS words; package words that are in the NS bag of words become FIXED.
	for key in package:
		code = package[key][0]
		if code == 'UNFIXED':
			w = package[key][1]
			if w in NSbag:
				package[key] = ['FIXED', w]
			else: pass
		else: pass
	return package

def get_spelling_suggestions(package):
	##this gets spelling suggestions for UNFIXED words; ; returns the updated package
	for key in package:
		code = package[key][0]
		raw = package[key][1]
		if code == 'UNFIXED':
			filteredsuggestions = []
			allsuggestions = d.suggest(raw)
			loweredsugs = []
			for b in allsuggestions:
				b = b.lower()
				if b not in loweredsugs:
					##this eliminates duplicates; d.suggest('bear') = [ ... 'Beard', 'bear', ...]; I may want to change this part later to remove any uppercased words (proper nouns, acronyms, etc.)
					loweredsugs.append(b)
			package[key] = ['UNFIXED', raw, loweredsugs]
			for sug in loweredsugs:
				#print sug
				##if sug in NSbag or sug in stopwords: ##i'm not sure what the best way to implement a check against both lists is... it's possible that one list is more important than the other and each word should be checked against the entire first list before any word is checked against the second, or some such scenario... but for now, I'm checking them both at once... ###After a cursory glance at an initial run, I decided assuming a stopword to be correct here is a bad approach-- For the sentence, 'The bird got shot dead.' all the resulting candidate sentences had 'got' replaced by 'not', because 'not' is a stopword. This is undesirable.
				if sug in NSbag:
					package[key] = ['FIXED', sug]
					break
				else: pass
		else: pass
	return package

def get_stats(package, globalstuff):
	pwords = len(package)
	pfixed = 0
	punfixed = 0
	##only for getting some statistics used in the paper
	for key in package:
		code = package[key][0]
		if code == 'FIXED':
			pfixed +=1
		if code == 'UNFIXED':
			punfixed +=1
	globalwords = globalstuff[0]
	globalfixed = globalstuff[1]
	globalunfixed = globalstuff[2]
	globalwords += pwords
	globalfixed += pfixed
	globalunfixed += punfixed
	globalstuff = [globalwords, globalfixed, globalunfixed]
	print 'PWORDS: \t', pwords, '\tPFIXED:\t', pfixed, '\tPUNFIXED:\t', punfixed
	print 'GLOBALWORDS: \t', globalwords, '\tGLOBALFIXED:\t', globalfixed, '\tGLOBALUNFIXED:\t', globalunfixed
	return globalstuff
		

def package_to_plist(package):
	##this converts the package to a list containing lists; each inner list represents one word position in the sentence and may contain a single word (for FIXED words) or multiple words (for UNFIXED words).
	plist = []
	counter = 0
	while counter < len(package):
		code = package[counter][0]
		if code == 'UNFIXED':
			plist.append(package[counter][2])
		else:
			plist.append([package[counter][1]])
		counter+=1
	return plist

def get_candidate_sentences(mylist, candidates, idx):
	if idx == len(mylist):
		cstripped = []
		for c in candidates:
			c = c.strip()
			cstripped.append(c)
		return cstripped
		#return candidates
	newcandidates = []
	for w in mylist[idx]:
		for c in candidates:
			if c+' '+w not in newcandidates:
				newcandidates.append(c+' '+w)
	return get_candidate_sentences(mylist, newcandidates, idx+1)



##main program
NSbag = get_bag(NSraw)
#The man happy when he drawes the picture maybe he likes her.
#NS_temp_bag=['happy', 'draws', 'when', 'maybe', 'likes']
NS_temp_bag=[]
NSbag=NSbag+NS_temp_bag


#itemnumber = '01'
itemnumber = item.split('item')
itemnumber = filter(None, itemnumber)
itemnumber = itemnumber[-1]
rawsentnum = 1
#globalwords = 0
#globalfixed = 0
#globalunfixed = 0
globalstuff = [0, 0, 0]

for rawsentence in NNSraw:
	orig_sent = ' '.join(word_tokenize(rawsentence.lower()))
	package = make_package(rawsentence)
	#print package
	package = package_vs_stopwords(package)
	#print package
	package = package_vs_NSbag(package)
	#print package
	package = get_spelling_suggestions(package)
	#print package
	globalstuff = get_stats(package, globalstuff)
	plist = package_to_plist(package)
	candidates = get_candidate_sentences(plist, [''], 0)
	candidates.insert(0, orig_sent)
	candnum = 0
	cs_index_name = ''.join([itemnumber, '_', "%03d"%rawsentnum, '_index.txt'])
	cs_index = open(''.join(['../data/cs_indices/', item, '/', cs_index_name]), 'w') #yes
	for c in candidates:
		filename = ''.join([itemnumber, '_', "%03d"%rawsentnum, '_', "%04d"%candnum, '.txt'])
		cs_index.write(''.join(['../../../data/candidate_sentences/', item, '/', filename, '\n'])) #this should be the path from the "scripts" directory
		outfile = open(''.join(['../data/candidate_sentences/', item, '/', filename]), 'w')
		outfile.write(c)
		outfile.close()
		candnum+=1
	rawsentnum+=1
			

#package = make_package(rawsentence)
##print package
#package = package_vs_stopwords(package)
##print package
#package = package_vs_NSbag(package)
##print package
#package = get_spelling_suggestions(package)
##print package

#package = {0: ['FIXED', 'A'], 1: ['FIXED', 'man'], 2: ['FIXED', 'is'], 3: ['FIXED', 'shooting'], 4: ['UNFIXED', 'z', ['a', 'I']], 5: ['UNFIXED', 'beerd', ['beard', 'beer', 'bear', 'bird']], 6: ['FIXED', '.']}
#package = {0: ['FIXED', 'A'], 1: ['FIXED', 'man'], 2: ['FIXED', 'is'], 3: ['FIXED', 'shooting'], 4: ['FIXED', 'a'], 5: ['FIXED', 'bird'], 6: ['FIXED', '.']}

#for c in candidates:
#	print c










####General notes on this code and problems encountered w.r.t it:
####NOTE THE FOLLOWING:
####>>> tokenize("A couple didn't watch T.V. last night.")
####word_tokenize yields:
####['A', 'couple', 'did', "n't", 'watch', 'T.V.', 'last', 'night', '.']
####>>> tokenize("A man should've walked more carefully.")
####word_tokenize yields:
####['A', 'man', 'should', "'ve", 'walked', 'more', 'carefully', '.'] 
####
####We see here that word_tokenize splits contractions into separate words; This may or may not be a problem depending on how SLM Toolkit hanldes contractions; I have a suspicion that it does not split these. Also, we'll need to consider how enchant/Aspell handle contractions:
####>>> d = enchant.Dict('en')
####>>> d.suggest("shouldn't")
####["shouldn't", "couldn't", "wouldn't"]
####
####OK-- so now we see that enchant does NOT split contractions.
####HOWEVER-- at this point, I believe there are NO CONTRACTIONS in the data set... so I can overlook this for now, but it will likely need to be addressed in the future!