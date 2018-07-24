#!/usr/bin/env python

##2016/06/10. LK. This version produces concatenated dependencies from a lemmatized conll file; this one also includes the head and dependent POS tags; e.g., "subj$@%kick~^VBD$@%boy~^NN"

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

# Note that a single sentence from the *.lemma_conll file looks like this:
# 1	a	_	DT	DT	_	2	det	_	_
# 2	boy	_	NN	NN	_	4	nsubj	_	_
# 3	be	_	VBZ	VBZ	_	4	aux	_	_
# 4	kick	_	VBG	VBG	_	0	root	_	_
# 5	a	_	DT	DT	_	6	det	_	_
# 6	ball	_	NN	NN	_	4	dobj	_	_
# 7	.	_	.	.	_	4	punct	_	_
#

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

pos_set =[]
all_sents = []
for cs in conllsents:
	current_sent = []
	for wline in cs:
		wlist = wline.split()
		depword, deppos, headindex, label = wlist[1], wlist[3], int(wlist[6]), wlist[7]
		if deppos not in pos_set: pos_set.append(deppos)
		if headindex == 0 and label == "root":
			head = "VROOT"
			headpos = "NONE"
		elif headindex == 0 and label == "erased":
			head = "WORDERASED"
			headpos = "NONE"
		else:
			#headline = cs[(headindex-1)]
			head = cs[(headindex-1)].split()[1]
			headpos = cs[(headindex-1)].split()[3]
			if headpos not in pos_set: pos_set.append(headpos)
		current_sent.append([label, depword, deppos, head, headpos])
	all_sents.append(current_sent)

all_ldh=[]
all_xdh=[]
all_ldx=[]
all_lxh=[]
all_xdx=[]

js="$@%"
ps="~^"
for pentsent in all_sents:
	ldh_list=[]
	xdh_list=[]
	ldx_list=[]
	lxh_list=[]
	xdx_list=[]
	for p in pentsent: ##[label, depword, deppos, head, headpos]
		ldh = p[0]+js+p[1]+ps+p[2]+js+p[3]+ps+p[4]
		ldh_list.append(ldh)
		xdh = 'x'+js+p[1]+ps+p[2]+js+p[3]+ps+p[4]
		xdh_list.append(xdh)
		ldx = p[0]+js+p[1]+ps+p[2]+js+'x'+ps+'NONE'
		ldx_list.append(ldx)
		lxh = p[0]+js+'x'+ps+'NONE'+js+p[3]+ps+p[4]
		lxh_list.append(lxh)
		xdx = 'x'+js+p[1]+ps+p[2]+js+'x'+ps+'NONE'
		xdx_list.append(xdx)
	all_ldh.append(ldh_list)
	all_xdh.append(xdh_list)
	all_ldx.append(ldx_list)
	all_lxh.append(lxh_list)
	all_xdx.append(xdx_list)

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

xdxfile=open(fileprefix+".xdx", 'w+')
for k in all_xdx:
	k = " ".join(k)
	xdxfile.write(k)
	xdxfile.write('\n')
xdxfile.close()

print pos_set