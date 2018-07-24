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

testdir=$1
refdir=$2
resultdir=$testdir\_$refdir\_results
mkdir -p $resultdir
deptypes=(ldh lxh ldx lxx xdh xdx xxh)

for dt in ${deptypes[@]} ; do mytests=$(ls $testdir/$dt) ; for myt in $mytests ; do python lk_tfidf.py $testdir/$dt/$myt $refdir/$dt > $resultdir/$myt\_$refdir.results ; done ; done
#
###(from lk_tfidf.py):
###testdocname = sys.argv[1]
####mycorpusdir = sys.argv[2]
###corpusdocname = sys.argv[2]
