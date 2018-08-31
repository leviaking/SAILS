#!/usr/bin/env bash

##2018-08-14. LK. This shell script simply runs the lk_tfidf_LOO_TC.py on each GS-depstrings-csv file in the depstrings folder (These files are the output of prep_conll_for_tfidf.py / prep_conll_for_tfidf.sh)
##USAGE:
##./lk_tfidf_LOO_TC.sh GS_depstrings_folder
##GS_depstrings_folder is '/Users/leviking/Documents/dissertation/SAILS/gold_standards/depstrings/'
##So relative to the current script folder, it's ../gold_standards/depstrings
##./lk_tfidf_LOO_TC.sh ../gold_standards/depstrings


scriptdir=$(pwd)
gsdir=$1
cd $gsdir
mygss=$(ls *.csv)
cd $scriptdir

for gs in $mygss ; do python lk_tfidf_LOO_TC.py $gsdir/$gs ; done 

scriptdir=$(pwd)
gsdir=../gold_standards/depstrings
cd $gsdir
mygss=$(ls *.csv)
cd $scriptdir