#!/usr/bin/env python

## 2015/07/14. LK. This script iterates over a conll file (10 column conll), extracts dependency triples, then joins them as a single string. See also: lemmatize_conll.py. This script should take the output of lemmatize_conll.py, which is a lemmatized conll file, then prepare strings of the following form for the purpose of doing dependency-based tf-idf with an existing tool. In other words, we're doing tf-idf, but the atomic unit here is not a TERM but a DEPENDENCY.

##USAGE:
##python prep_conll_for_tfidf.py myfile.lemma_conll

# consider: subj, kick, boy
#  label_dep_head # subj_kick_boy #l_d_h
#  *_dep_head # *_kick_boy #x_d_h
#  label_dep_* # subj_kick_* #l_d_x
#  label_*_head # subj_*_boy #l_x_h
#  label_*_* # subj_*_* #l_x_x (I really doubt this one is infomative...)
#  *_dep_* # *_kick_* #x_d_x
#  *_*_head # *_*_boy #x_x_h

import sys, os

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

all_ldh=[]
all_xdh=[]
all_ldx=[]
all_lxh=[]
all_lxx=[]
all_xdx=[]
all_xxh=[]

js="$@%"
for tripsent in all_sents:
	ldh_list=[]
	xdh_list=[]
	ldx_list=[]
	lxh_list=[]
	lxx_list=[]
	xdx_list=[]
	xxh_list=[]
	for trip in tripsent:
		ldh = js.join([trip[0], trip[1], trip[2]])
		ldh_list.append(ldh)
		xdh = js.join(['x', trip[1], trip[2]])
		xdh_list.append(xdh)
		ldx = js.join([trip[0], trip[1], 'x'])
		ldx_list.append(ldx)
		lxh = js.join([trip[0], 'x', trip[2]])
		lxh_list.append(lxh)
		lxx = js.join([trip[0], 'x', 'x'])
		lxx_list.append(lxx)
		xdx = js.join(['x', trip[1], 'x'])
		xdx_list.append(xdx)
		xxh = js.join(['x', 'x', trip[2]])
		xxh_list.append(xxh)
	all_ldh.append(ldh_list)
	all_xdh.append(xdh_list)
	all_ldx.append(ldx_list)
	all_lxh.append(lxh_list)
	all_lxx.append(lxx_list)
	all_xdx.append(xdx_list)
	all_xxh.append(xxh_list)

#for k in all_ldh:
#	k = " ".join(k)
#	print k, '\n'
#	
ldhfile=open(fileprefix+".ldh", 'w+')
for k in all_ldh:
	k = " ".join(k)
	ldhfile.write(k)
	ldhfile.write('\n')
ldhfile.close()

xdhfile=open(fileprefix+".xdh", 'w+')
for k in all_xdh:
	k = " ".join(k)
	xdhfile.write(k)
	xdhfile.write('\n')
xdhfile.close()

ldxfile=open(fileprefix+".ldx", 'w+')
for k in all_ldx:
	k = " ".join(k)
	ldxfile.write(k)
	ldxfile.write('\n')
ldxfile.close()

lxhfile=open(fileprefix+".lxh", 'w+')
for k in all_lxh:
	k = " ".join(k)
	lxhfile.write(k)
	lxhfile.write('\n')
lxhfile.close()

lxxfile=open(fileprefix+".lxx", 'w+')
for k in all_lxx:
	k = " ".join(k)
	lxxfile.write(k)
	lxxfile.write('\n')
lxxfile.close()

xdxfile=open(fileprefix+".xdx", 'w+')
for k in all_xdx:
	k = " ".join(k)
	xdxfile.write(k)
	xdxfile.write('\n')
xdxfile.close()

xxhfile=open(fileprefix+".xxh", 'w+')
for k in all_xxh:
	k = " ".join(k)
	xxhfile.write(k)
	xxhfile.write('\n')
xxhfile.close()
