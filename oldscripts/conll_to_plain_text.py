#!/usr/bin/env python

## 2015/07/13. LK. This script takes a .conll file as input; pulls the words out of the conll file and joins them together as plain text sentences, one sentence per line. ##NOTE: Sentences with multiple consecutive punctuation characters are problematic, so they are skipped and will not be included in the resulting text file. 

import sys, re

conllname=sys.argv[1]

conllsents = []
with open(conllname) as conllfile:
	current_csent = []
	for cline in conllfile:
		cline = cline.strip()
		if cline == '':
			pass
		else:		
			if cline.startswith('1\t') and current_csent: ## "and current_csent" bc we don't want to append the empty list when we initialize on the first line
				conllsents.append(current_csent)
				current_csent=[cline]
			else:
				current_csent.append(cline)
	conllsents.append(current_csent)

text_sents = [] #plain text versions of the conll sentences.
while conllsents:
	tsentlist = []
	csent = conllsents.pop(0)
	while csent:
		cwline = csent.pop(0)
		cwlist = cwline.split('\t')
		cword = cwlist[1]
		cword = re.sub('-LRB-|-lrb', "(", cword)
		cword = re.sub('-RRB-|-rrb', ")", cword)
		cword = re.sub(r"\\/", "/", cword)
		cword = re.sub("``", '"', cword)
		cword = re.sub("''", '"', cword)
		#print cword
		tsentlist.append(cword)
	# for t in tsentlist:
	# 	print t
	# print '\n'
	if len(tsentlist) >= 2 and re.match('\W+', tsentlist[-1]):
		lastwd = tsentlist.pop()
		nextlastwd = tsentlist.pop()
		combined = ''.join([nextlastwd, lastwd])
		tsentlist.append(combined)
	else: pass
	text_sent = ' '.join(tsentlist)
	text_sents.append(text_sent)

for ts in text_sents:
	print ts
