###TOTALLY IGNORE#!/bin/bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

#scriptdir=`dirname $0`

###NOTE: This script requires Bash 4 or above (because it uses the readarray command)

##This script takes a file of plain text, with one sentence per line. It parses this text file with Stanford (to constituency and dependency). It also processes the text file with the stanford core-nlp lemmatizer, generating an xml file. It takes the newly parsed .conll file and the xml/lemmatized file, and replaces the conll words with their lemmatized counterparts, writing out a new file as "whatever.lemma_conll".

##HOW TO RUN THIS SCRIPT: Get this directory set up:
##dissertation/
##	SAILS/
##		scripts/
##			gscsv_to_lemmatized_conll.sh
##			gscsv_to_txt.py
##			lemmatize_conll.py
##		gold_standards/
##			I01T_all_ns.csv [etc]
##			txt/
##				I01T_all_ns.txt [etc; these are generated by this script]
##	SAILS_annex/
##		stanford-parser-2012-01-06/
##		stanford-corenlp-full-2014-06-16/

##The first command parses raw text to PTB style constituency trees; the second takes these trees and converts them to dependencies (typed, collapsed, and with propagated conjunctions; modify the stanford command options to change these parameters) printed in CoNLL format.

scriptdir=$(pwd)
#echo $scriptdir
cd ../
rawcsvdir=$(pwd)/gold_standards/rawcsvs
textdir=$(pwd)/gold_standards/txt
lemmaxmldir=$(pwd)/gold_standards/lemmaxml
penndir=$(pwd)/gold_standards/penn
lkconlldir=$(pwd)/gold_standards/LKconll
cd ../
parserdir=$(pwd)/SAILS_annex/stanford-parser-2012-01-06
lemmatizerdir=$(pwd)/SAILS_annex/stanford-corenlp-full-2014-06-16
#echo $scriptdir
#echo $rawcsvdir
#echo $parserdir
#echo $lemmatizerdir
cd $rawcsvdir
#allcsvs=($(ls .))
#echo ${allcsvs[@]}
allcsvs=(
#I01T_all_ns.csv
#I01U_all_ns.csv
#I02T_all_ns.csv
#I02U_all_ns.csv
#I03T_all_ns.csv
#I03U_all_ns.csv
#I04T_all_ns.csv
#I04U_all_ns.csv
#I05T_all_ns.csv
#I05U_all_ns.csv
#I06T_all_ns.csv
#I06U_all_ns.csv
#I07T_all_ns.csv
#I07U_all_ns.csv
#I08T_all_ns.csv
#I08U_all_ns.csv
#I09T_all_ns.csv
#I09U_all_ns.csv
#I10T_all_ns.csv
#I10U_all_ns.csv
#I11T_all_ns.csv
#I11U_all_ns.csv
#I12T_all_ns.csv
#I12U_all_ns.csv
#I13T_all_ns.csv
#I13U_all_ns.csv
#I14T_all_ns.csv
#I14U_all_ns.csv
#I15T_all_ns.csv
#I15U_all_ns.csv
#I16T_all_ns.csv
#I16U_all_ns.csv
#I17T_all_ns.csv
#I17U_all_ns.csv
#I18T_all_ns.csv
#I18U_all_ns.csv
#I19T_all_ns.csv
#I19U_all_ns.csv
#I20T_all_ns.csv
#I20U_all_ns.csv
I21T_all_ns.csv
#I21U_all_ns.csv
#I22T_all_ns.csv
#I22U_all_ns.csv
#I23T_all_ns.csv
#I23U_all_ns.csv
#I24T_all_ns.csv
#I24U_all_ns.csv
#I25T_all_ns.csv
#I25U_all_ns.csv
#I26T_all_ns.csv
#I26U_all_ns.csv
#I27T_all_ns.csv
#I27U_all_ns.csv
#I28T_all_ns.csv
#I28U_all_ns.csv
#I29T_all_ns.csv
#I29U_all_ns.csv
#I30T_all_ns.csv
#I30U_all_ns.csv
)

#for c in ${allcsvs[@]}; do echo $c ; done

cd $scriptdir


for mycsv in ${allcsvs[@]}
	do label=${mycsv/.csv/}
	mytext=$textdir/$label.txt
	mylemmaxml=$lemmaxmldir/$label.xml
	python $scriptdir/gscsv_to_txt.py $rawcsvdir/$mycsv
	##echo $label
	##echo $mytext
	cd $lemmatizerdir
	####the following lines and the for loop are my hacky and less-than-ideal work around for the following:
	##this was the old command##java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file $mytext -outputDirectory $lemmaxmldir
	##LK: I cannot find a way to force the Stanford CoreNLP tool to handle each line as a sentence. For some sentence fragments, it combines the fragment with the subsequent line. For example:
	##The b.
	##Getting ready to take a bite of pizza.
	##The two responses above get combined in the lemmatized output. This is a problem because I cannot then align the lemmatized output with the (correct) parsed output. I think I am now forced to somehow load the lemmatizer anew for each line so that it has no choice but to handle each line as a single sentence.	The following lines do this.
	readarray respies < $mytext
	tempcounter=1
	for respy in "${respies[@]}"
		do padded=$(printf %03d $tempcounter)
		echo $respy > $textdir/lemmatizer_temp.txt
		#cat $textdir/lemmatizer_input_temp.txt
		java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file $textdir/lemmatizer_temp.txt -outputDirectory $lemmaxmldir -outputExtension $padded
		cat $lemmaxmldir/lemmatizer_temp.txt$padded >> $mylemmaxml
		rm $lemmaxmldir/lemmatizer_temp.txt$padded
		rm $textdir/lemmatizer_temp.txt
		tempcounter=$((tempcounter + 1))
		#do echo $respy
		done
	####back to normal below...
	cd $parserdir
	java -mx800m -cp "stanford-parser.jar:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat "penn" -outputFormatOptions "CCPropagatedDependencies" $parserdir/grammar/englishPCFG.ser.gz $mytext > $penndir/$label.penn
	java -mx800m -cp "$parserdir/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $penndir/$label.penn -conllx -CCprocessed > $lkconlldir/$label.LKconll
	python $scriptdir/lemmatize_conll.py $mytext
	done
