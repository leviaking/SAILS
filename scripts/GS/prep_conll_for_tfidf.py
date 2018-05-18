#!/usr/bin/env python

## 2015/07/14. LK. This script iterates over a conll file (10 column conll), extracts dependency triples, then joins them as a single string. See also: lemmatize_conll.py. This script should take the output of lemmatize_conll.py, which is a lemmatized conll file, then prepare strings of the following form for the purpose of doing dependency-based tf-idf with an existing tool. In other words, we're doing tf-idf, but the atomic unit here is not a TERM but a DEPENDENCY.

##USAGE:
##python prep_conll_for_tfidf.py myfile.lemma_conll

# consider: subj, kick, boy
#  label_head_dep # subj_kick_boy #l_h_d
#  *_head_dep # *_kick_boy #x_h_d
#  label_head_* # subj_kick_* #l_h_x
#  label_*_dep # subj_*_boy #l_x_d
#  label_*_* # subj_*_* #l_x_x (I really doubt this one is infomative...)
#  *_head_* # *_kick_* #x_h_x
#	*_*_dep # *_*_boy #x_x_d

import sys

conllname = sys.argv[1]
fileprefix = conllname.split('.')[0]

conllsents = []
ccounter = 1
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
#for c in conllsents:
#	for d in c:
#		print d
#	print ""

all_sents = []
for cs in conllsents:
	current_sent = []
	for wline in cs:
		wlist = wline.split()
		word, headindex, label = wlist[1], int(wlist[6]), wlist[7]
		if headindex == 0 and label == "root":
			head = "VROOT"
		elif headindex == 0 and label == "erased":
			head = "WORDERASED"
		else:
			#headline = cs[(headindex-1)]
			head = cs[(headindex-1)].split()[1]
		current_sent.append([label, word, head])
	all_sents.append(current_sent)

all_lhd=[]
all_xhd=[]
all_lhx=[]
all_lxd=[]
all_lxx=[]
all_xhx=[]
all_xxd=[]

js="$@%"
for tripsent in all_sents:
	lhd_list=[]
	xhd_list=[]
	lhx_list=[]
	lxd_list=[]
	lxx_list=[]
	xhx_list=[]
	xxd_list=[]
	for trip in tripsent:
		lhd = js.join([trip[0], trip[1], trip[2]])
		lhd_list.append(lhd)
		xhd = js.join(['x', trip[1], trip[2]])
		xhd_list.append(xhd)
		lhx = js.join([trip[0], trip[1], 'x'])
		lhx_list.append(lhx)
		lxd = js.join([trip[0], 'x', trip[2]])
		lxd_list.append(lxd)
		lxx = js.join([trip[0], 'x', 'x'])
		lxx_list.append(lxx)
		xhx = js.join(['x', trip[1], 'x'])
		xhx_list.append(xhx)
		xxd = js.join(['x', 'x', trip[2]])
		xxd_list.append(xxd)
	all_lhd.append(lhd_list)
	all_xhd.append(xhd_list)
	all_lhx.append(lhx_list)
	all_lxd.append(lxd_list)
	all_lxx.append(lxx_list)
	all_xhx.append(xhx_list)
	all_xxd.append(xxd_list)

#for k in all_lhd:
#	k = " ".join(k)
#	print k, '\n'
#	
lhdfile=open(fileprefix+".lhd", 'w+')
for k in all_lhd:
	k = " ".join(k)
	lhdfile.write(k)
	lhdfile.write('\n')
lhdfile.close()

xhdfile=open(fileprefix+".xhd", 'w+')
for k in all_xhd:
	k = " ".join(k)
	xhdfile.write(k)
	xhdfile.write('\n')
xhdfile.close()

lhxfile=open(fileprefix+".lhx", 'w+')
for k in all_lhx:
	k = " ".join(k)
	lhxfile.write(k)
	lhxfile.write('\n')
lhxfile.close()

lxdfile=open(fileprefix+".lxd", 'w+')
for k in all_lxd:
	k = " ".join(k)
	lxdfile.write(k)
	lxdfile.write('\n')
lxdfile.close()

lxxfile=open(fileprefix+".lxx", 'w+')
for k in all_lxx:
	k = " ".join(k)
	lxxfile.write(k)
	lxxfile.write('\n')
lxxfile.close()

xhxfile=open(fileprefix+".xhx", 'w+')
for k in all_xhx:
	k = " ".join(k)
	xhxfile.write(k)
	xhxfile.write('\n')
xhxfile.close()

xxdfile=open(fileprefix+".xxd", 'w+')
for k in all_xxd:
	k = " ".join(k)
	xxdfile.write(k)
	xxdfile.write('\n')
xxdfile.close()
