#!/usr/bin/env bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

scriptdir=`dirname $0`

##This script runs prep_conll_for_tfidf.py on each of the *.lemma_conll files in the target folder. After processing all the files, it cleans up the folder -- It finds the file extension of each file; it creates a folder for any extension that does not already have a folder, then it moves each file into its matching directory.

##HOW TO RUN THIS SCRIPT:
##./prep_conll_for_tfidf.sh testfolder
##(testfolder should be directly inside folder containing this script)

testdir=$1

cd $testdir
lemcons=$(ls *.lemma_conll)
cd ..

for lemcon in ${lemcons[@]} ; do python prep_conll_for_tfidf.py $testdir/$lemcon ; done

cd  $testdir
allexts=(dummy)
${alltexts[@]}
allfiles=$(ls *.*)
for af in ${allfiles[@]} ; do afext=${af##*.} ; allexts=(${allexts[@]} $afext) ; done
uniqexts=($(printf "%s\n" "${allexts[@]}" | sort -u)); echo "${uniq[@]}"
uniqexts=(${uniqexts[@]/dummy/})
for ext in ${uniqexts[@]} ; do mkdir -p $ext ; for afile in $(ls *.$ext) ; do mv $afile $ext/$afile ; done ; done
