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

lc_dir=$1/lemma_conll

cd $lc_dir
lemcons=$(ls *.lemma_conll)
cd ../..

for lemcon in ${lemcons[@]} ; do python prep_conll_for_tfidf_include_POS.py $lc_dir/$lemcon ; done

cd  $lc_dir
allexts=(ldh xdh lxh ldx xdx)
posdirpref=posdep
#${alltexts[@]}
#allfiles=$(ls *.*)
#for af in ${allfiles[@]} ; do afext=${af##*.} ; allexts=(${allexts[@]} $afext) ; done
#uniqexts=($(printf "%s\n" "${allexts[@]}" | sort -u)); echo "${uniq[@]}"
#uniqexts=(${uniqexts[@]/dummy/})
mkdir ../posdep
for ext in ${allexts[@]} ; do mkdir -p ../$posdirpref/$ext ; for afile in $(ls *.$ext) ; do mv $afile ../$posdirpref/$ext/$afile ; done ; done
