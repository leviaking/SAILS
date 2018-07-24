#!/usr/bin/env bash

#if [ ! $# -ge 1 ]; then
#  echo Usage: `basename $0` 'file(s)'
#  echo
#  exit
#fi

#scriptdir=`dirname $0`

##2018-07-20 update. I'm modifying this script to work on the lemma-parse csv files. See them here: /Users/leviking/Documents/dissertation/SAILS/gold_standards/finalcsvs

##NOTICE: Name change: In the 2015-2016 SAILS work, this shell script was called prep_conll_for_tfidf.sh and the python script it calls was called prep_conll_for_tfidf.py


####This script runs prep_conll_for_tfidf.py on each of the *.lemma_conll files in the target folder. After processing all the files, it cleans up the folder -- It finds the file extension of each file; it creates a folder for any extension that does not already have a folder, then it moves each file into its matching directory.

####HOW TO RUN THIS SCRIPT:
####./prep_conll_for_tfidf.sh testfolder
####(testfolder should be directly inside folder containing this script)

scriptdir=$(pwd)
cd ../
goldrootdir=$(pwd)/gold_standards/
depstringsdir=$goldrootdir/depstrings/

if [ ! -d "$depstringsdir" ]; then
	# Control will enter here if $DIRECTORY doesn't exist.
	mkdir $depstringsdir
fi

cd $goldrootdir

rawcsvdir=$(pwd)/rawcsvs
textdir=$(pwd)/txt
lemmaxmldir=$(pwd)/lemmaxml
penndir=$(pwd)/penn
lkconlldir=$(pwd)/LKconll
gslemcondir=$(pwd)/finalcsvs
#
cd ../..
parserdir=$(pwd)/SAILS_annex/stanford-parser-2012-01-06
lemmatizerdir=$(pwd)/SAILS_annex/stanford-corenlp-full-2014-06-16
cd $gslemcondir
gslemcons=$(ls *.csv)
cd $scriptdir

for gslemcon in ${gslemcons[@]} ; do python prep_conll_for_tfidf.py $testdir/$gslemcon ; done
#for gslemcon in ${gslemcons[@]} ; do echo $testdir/$gslemcon ; done

#cd  $testdir
#allexts=(dummy)
#${alltexts[@]}
#allfiles=$(ls *.*)
#for af in ${allfiles[@]} ; do afext=${af##*.} ; allexts=(${allexts[@]} $afext) ; done
#uniqexts=($(printf "%s\n" "${allexts[@]}" | sort -u)); echo "${uniq[@]}"
#uniqexts=(${uniqexts[@]/dummy/})
#for ext in ${uniqexts[@]} ; do mkdir -p $ext ; for afile in $(ls *.$ext) ; do mv $afile $ext/$afile ; done ; done
