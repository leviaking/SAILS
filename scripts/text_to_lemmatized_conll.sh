#!/usr/bin/env bash

##if [ ! $# -ge 1 ]; then
##  echo Usage: `basename $0` 'file(s)'
##  echo
##  exit
##fi

scriptdir=`dirname $0`

#### BELOW: 2019/06/16. I don't know about all this below. Evaluate later.
##This script takes a file of plain text, with one sentence per line. It parses this text file with Stanford (to constituency and dependency). It also processes the text file with the stanford core-nlp lemmatizer, generating an xml file. It takes the newly parsed .conll file and the xml/lemmatized file, and replaces the conll words with their lemmatized counterparts, writing out a new file as "whatever.lemma_conll".

##HOW TO RUN THIS SCRIPT: Put this script, the python script, and the folder containing the text file(s) to process in the same folder containing the two stanford tools folders; i.e.:
##someparentfolder/
##	text_to_lemmatized_conll.sh
##	text_to_lemmatized_conll.py
##	folder_of_raw_text_files/
##	stanford-corenlp-full-2014-06-16/
##	stanford-parser-2012-01-06/
##	
##You need to follow the script name with the foldername of the text you want to parse. Example:
###./text_to_lemmatized_conll.sh mytexts/
##The first command parses raw text to PTB style constituency trees; the second takes these trees and converts them to dependencies (typed, collapsed, and with propagated conjunctions; modify the stanford command options to change these parameters) printed in CoNLL format.
#### ABOVE: 2019/06/16. I don't know about all this above. Evaluate later.


## First step here is to run response_csv_to_txt.py on all master_anno corpus files; this pulls the NNS entries from the master_anno file and then does two things with them: 1. It saves the text of the response to a .txt file, one sentence per line (this is the easiest format to pass through stanford parser); 2. It saves Response, ResponseID, C, A, G, I, V (annotations) to "rawcsv" file.
## List all the master_anno files so we can iterate over them:
##all_master_annos=$(ls ../corpus/*master_anno.csv)
##for ma in ${all_master_annos[@]}
##  do echo $ma
##  python response_csv_to_txt.py $ma
##  done
## 2019/06/16. Above is completed and should not be repeated.


##textdir=$1
textdir=../responses/txt


scriptdir=$(pwd)
#echo $scriptdir
cd ../
rawcsvdir=$(pwd)/responses/rawcsvs
textdir=$(pwd)/responses/txt
lemmaxmldir=$(pwd)/responses/lemmaxml
penndir=$(pwd)/responses/penn
lkconlldir=$(pwd)/responses/LKconll
cd ../
parserdir=$(pwd)/SAILS_annex/stanford-parser-2012-01-06
lemmatizerdir=$(pwd)/SAILS_annex/stanford-corenlp-full-2014-06-16

cd $textdir
alltexts=$(ls *.txt)
declare -A item_cache  # initialize so "unset" doesn't fail on first pass
for mytext in ${alltexts[@]} # ; do echo $mytext; done
  do cd $lemmatizerdir
	label=${mytext/.txt/}  ## filename minus file extension
  unset item_cache
  declare -A item_cache
  echo "### Beginning lemmatization of current file: "$mytext" ###"
	mylemmaxml=$lemmaxmldir/$label.xml
  tempcounter=1
	readarray respies < $textdir/$mytext
	for respy in "${respies[@]}"
    do padded=$(printf %03d $tempcounter)
    echo "# Checking cache for current response: "$respy" #"
    if [[ ${item_cache[$respy]} ]]
    then
      echo "# Exists in cache; pulling lemmatized response"
      echo ${item_cache[$respy]} >> $mylemmaxml
    else
      echo "# Doesn't exist in cache; running lemmatizer #"
      echo $respy > $textdir/lemmatizer_temp.txt
      #cat $textdir/lemmatizer_input_temp.txt
      java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file $textdir/lemmatizer_temp.txt -outputDirectory $lemmaxmldir -outputExtension $padded
      cat $lemmaxmldir/lemmatizer_temp.txt$padded >> $mylemmaxml
      cacheable="$(cat $lemmaxmldir/lemmatizer_temp.txt$padded)"
      ##echo "CACHEABLE"
      ##echo $cacheable
      rm $lemmaxmldir/lemmatizer_temp.txt$padded
      rm $textdir/lemmatizer_temp.txt
      item_cache["${respy}"]="$cacheable"
    fi
		tempcounter=$((tempcounter + 1))
		#do echo $respy
  done
  ##for K in "${!item_cache[@]}"; do echo $K; done
  ##echo "Here are all the cached responses:"
  ##echo "${!item_cache[@]}"
	cd $parserdir
  echo "## Beginning constituency parse of current file: "$mytext" ##"
	java -mx800m -cp "stanford-parser.jar:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat "penn" -outputFormatOptions "CCPropagatedDependencies" $parserdir/grammar/englishPCFG.ser.gz $textdir/$mytext > $penndir/$label.penn
  echo "## Beginning dependency parse of current file: "$mytext" ##"
	java -mx800m -cp "$parserdir/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $penndir/$label.penn -conllx -CCprocessed > $lkconlldir/$label.LKconll
  echo "## Merging lemmatized text with dependency parse for current file: "$mytext" ##"
	python $scriptdir/lemmatize_conll.py $textdir/$mytext
	done
