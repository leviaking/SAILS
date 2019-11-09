#!/usr/bin/env python

##2018-07-20 update. I'm modifying this script to work on the lemma-parse csv files. See them here: /Users/leviking/Documents/dissertation/SAILS/gold_standards/finalcsvs
##This script will write directly to the csv, with each of the given formats of "dependency strings" written to a new column in the csv.

##NOTICE: Name change: In the 2015-2016 SAILS work, this script was called prep_conll_for_tfidf.py and the shell script was called prep_conll_for_tfidf.sh

#### 2015/07/14. LK. This script iterates over a conll file (10 column conll), extracts dependency triples, then joins them as a single string. See also: lemmatize_conll.py. This script should take the output of lemmatize_conll.py, which is a lemmatized conll file, then prepare strings of the following form for the purpose of doing dependency-based tf-idf with an existing tool. In other words, we're doing tf-idf, but the atomic unit here is not a TERM but a DEPENDENCY.

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

import sys, re, csv, datetime, os
from shutil import copyfile

scriptdir = os.getcwd()

sourcename = sys.argv[1]
#print sourcename
handle = sourcename.split('.')[0]
#print handle
rootdir=os.path.dirname(scriptdir)
#print rootdir
sourcedir=rootdir+'/responses/finalcsvs'
destdir=rootdir+'/responses/depstrings'
source=sourcedir+sourcename
dest=destdir+handle+'_depstrings.csv'
#print source
js="$@%" ##this is the string we use to join the elements in a depstring; it's a delimiter



#print sourcename, destname

###2018-07-20

def form_depstrings(cs):
	ldh_list=[]
	#ldx_list=[]
	#_list=[]
	xdh_list=[]
	xdx_list=[]
	for trip in cs:
		ldh = js.join([trip[0], trip[1], trip[2]])
		ldh_list.append(ldh)
		#ldx = js.join([trip[0], trip[1], 'x'])
		#_list.append(ldx)
		#lxh = js.join([trip[0], 'x', trip[2]])
		#lxh_list.append(lxh)				
		xdh = js.join(['x', trip[1], trip[2]])
		xdh_list.append(xdh)
		xdx = js.join(['x', trip[1], 'x'])
		xdx_list.append(xdx)
	#print sds
	#sds=[ldh_list, ldx_list, lxh_list, xdh_list, xdx_list] ##sentence depstrings
	sds=[ldh_list, xdh_list, xdx_list] ##sentence depstrings
	return sds


def process_source_csv():
	with open(source, 'rU') as sourcefile, open(dest, 'w') as destfile:
		sourcereader=csv.reader(sourcefile, dialect=csv.excel)
		header=next(sourcereader, None)
		#header=header+['ldh', 'ldx', 'lxh', 'xdh', 'xdx']
		header=header+['ldh', 'xdh', 'xdx']
		destwriter=csv.writer(destfile, dialect=csv.excel)
		destwriter.writerow(header)
		for sline in sourcereader:
			current_sent=[]
			dline=list(sline)
			#annotations=cline[2:6]
			parse=sline[7].strip()
			#print parse, 'HI'
			parselines=parse.split('\n')
			#for wline in cs:
			for wline in parselines:
				wlist = wline.split()
				#print wlist
				word, headindex, label = wlist[1], int(wlist[6]), wlist[7]
				if headindex == 0 and label == "root":
					head = "VROOT"
				elif headindex == 0 and label == "erased":
					head = "WORDERASED"
				else:
					#headline = cs[(headindex-1)]
					head = parselines[(headindex-1)].split()[1]
				current_sent.append([label, word, head])
			sentdepstrings=form_depstrings(current_sent)
			dline=dline+sentdepstrings
			destwriter.writerow(dline)

process_source_csv()