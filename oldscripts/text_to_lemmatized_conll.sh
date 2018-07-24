#!/bin/bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

scriptdir=`dirname $0`

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

##mytext=$1
textdir=$1

cd $textdir
alltexts=$(ls *.txt)
cd ..

for mytext in ${alltexts[@]}
	do cd stanford-corenlp-full-2014-06-16 
	java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file ../$textdir/$mytext -outputDirectory ../$textdir
	cd ../$textdir
	mv $mytext.xml ${mytext/.txt/.xml}
	cd ..
	java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" -outputFormatOptions "CCPropagatedDependencies" $scriptdir/stanford-parser-2012-01-06/grammar/englishPCFG.ser.gz $textdir/$mytext > $textdir/${mytext/.txt/.penn}
	java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $textdir/${mytext/.txt/.penn} -conllx -CCprocessed > $textdir/${mytext/.txt/.LKconll}
	python lemmatize_conll.py $textdir/$mytext
	done
