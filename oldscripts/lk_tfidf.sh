#!/usr/bin/env bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

scriptdir=`dirname $0`

##This script runs lk_tfidf.py on each of the dependency string files in the test folder, comparing (and averaging) with the corresponding files in the reference corpus.

##HOW TO RUN THIS SCRIPT:
##./lk_tfidf.sh testfolder referencefolder
##(testdir is probably GS, NNSO or NNSLM; referencedir is probably wsj or brown)

testdir=$1
refdir=$2
resultdir=$testdir\_$refdir\_tfidf
mkdir -p $resultdir
deptypes=(ldh lxh ldx xdh xdx)

for dt in ${deptypes[@]} ; do mytests=$(ls $testdir/$dt) ; for myt in $mytests ; do python lk_tfidf.py $testdir/$dt/$myt $refdir/$dt > $resultdir/$myt\_$refdir.tfidf ; done ; done

#for dt in ${deptypes[@]} ; ##~= for deptype in (ldh lxh ldx lxx xdh xdx xxh)
	#do mytests=$(ls $testdir/$dt) ; ##mytests = list of all files in e.g. 'GS/ldh/' (these are ldh-formatted responses)
	#for myt in $mytests ; ##for file in list, e.g. "i01gs.ldh"
		#do cp $testdir/$dt/$myt $refdir/$dt/$myt ; ##copy test file to reference documents (intended to ensure that at least 1 token of the terms occurs in the ref corpus so that we don't try to divide by 0)
		#python lk_tfidf.py $testdir/$dt/$myt $refdir/$dt > $resultdir/$myt\_$refdir.results ; ##use the python script on the test document and reference corpus, then write results to the results file in the results directory
		#rm $refdir/$dt/$myt ; ##remove the test document from the reference corpus (we just added it there temporarily)
		#done ;
	#done




###(from lk_tfidf.py):
###testdocname = sys.argv[1]
####mycorpusdir = sys.argv[2]
###corpusdocname = sys.argv[2]
