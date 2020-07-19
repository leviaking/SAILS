#!/usr/bin/env bash

##2018-08-14. LK. This shell script simply runs the lk_tfidf_TC.py on each GS-depstrings-csv file in the depstrings folder (These files are the output of prep_conll_for_tfidf.py / prep_conll_for_tfidf.sh)
##USAGE:
##./lk_tfidf_LOO_TC.sh GS_depstrings_folder
##GS_depstrings_folder is '/Users/leviking/Documents/dissertation/SAILS/gold_standards/depstrings/'
##So relative to the current script folder, it's ../gold_standards/depstrings
##./lk_tfidf_LOO_TC.sh ../gold_standards/depstrings


scriptdir=$(pwd)
#gsdir=$1
##gsdir='/Users/leviking/Documents/dissertation/SAILS/gold_standards/depstrings/'
gsdir='/Users/leviking/Documents/dissertation/SAILS/gold_standards/cross-validation/depstrings/'

## These files are stored in /Users/leviking/Documents/dissertation/SAILS/responses/
mytestdocs=( I01T_NNS_depstrings.csv I02T_NNS_depstrings.csv I03T_NNS_depstrings.csv I04T_NNS_depstrings.csv I05T_NNS_depstrings.csv I06T_NNS_depstrings.csv I07T_NNS_depstrings.csv I08T_NNS_depstrings.csv I09T_NNS_depstrings.csv I10T_NNS_depstrings.csv I11T_NNS_depstrings.csv I12T_NNS_depstrings.csv I13T_NNS_depstrings.csv I14T_NNS_depstrings.csv I15T_NNS_depstrings.csv I16T_NNS_depstrings.csv I17T_NNS_depstrings.csv I18T_NNS_depstrings.csv I19T_NNS_depstrings.csv I20T_NNS_depstrings.csv I21T_NNS_depstrings.csv I22T_NNS_depstrings.csv I23T_NNS_depstrings.csv I24T_NNS_depstrings.csv I25T_NNS_depstrings.csv I26T_NNS_depstrings.csv I27T_NNS_depstrings.csv I28T_NNS_depstrings.csv I29T_NNS_depstrings.csv I30T_NNS_depstrings.csv I01U_NNS_depstrings.csv I02U_NNS_depstrings.csv I03U_NNS_depstrings.csv I04U_NNS_depstrings.csv I05U_NNS_depstrings.csv I06U_NNS_depstrings.csv I07U_NNS_depstrings.csv I08U_NNS_depstrings.csv I09U_NNS_depstrings.csv I10U_NNS_depstrings.csv I11U_NNS_depstrings.csv I12U_NNS_depstrings.csv I13U_NNS_depstrings.csv I14U_NNS_depstrings.csv I15U_NNS_depstrings.csv I16U_NNS_depstrings.csv I17U_NNS_depstrings.csv I18U_NNS_depstrings.csv I19U_NNS_depstrings.csv I20U_NNS_depstrings.csv I21U_NNS_depstrings.csv I22U_NNS_depstrings.csv I23U_NNS_depstrings.csv I24U_NNS_depstrings.csv I25U_NNS_depstrings.csv I26U_NNS_depstrings.csv I27U_NNS_depstrings.csv I28U_NNS_depstrings.csv I29U_NNS_depstrings.csv I30U_NNS_depstrings.csv)

for td in ${mytestdocs[@]}
do
	echo $(date)": Beginning: "$td
	python lk_tfidf_TC.py $td
done 
