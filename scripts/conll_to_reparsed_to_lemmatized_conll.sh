#!/usr/bin/env bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

scriptdir=`dirname $0`

##This script takes a .conll file, extracts the text from it as plain text and writes it out to a file, with one sentence per line. It then parses this text file again (because I've changed the parser parameters below). It also processes the text file with the stanford core-nlp lemmatizer, generating an xml file. It takes the newly parsed .conll file and the xml/lemmatized file, and replaces the conll words with their lemmatized counterpart, writing out a new file as "whatever.lemma_conll".

##HOW TO RUN THIS SCRIPT: Put this script and the conll files to process in a folder above the two stanford tools folders. You need to follow the script name with the name of this folder containing the conll files. Example:
###./conll_to_reparsed_to_lemmatized_conll.sh my_ptb
##The first command parses raw text to PTB style constituency trees; the second takes these trees and converts them to dependencies (typed, collapsed, and with propagated conjunctions; modify the stanford command options to change these parameters) printed in CoNLL format.

cd $1
myarray=$(ls *.conll)
cd ..

for myc in $myarray; do python conll_to_plain_text.py $1/$myc > "$1/${myc/.conll/.txt}" ; done

cd stanford-corenlp-full-2014-06-16

for myt in $(ls ../$1/*.txt); do echo $myt ; java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file ../$1/$myt -outputDirectory ../$1 ; done
##That should result in file $1/$myt.xml ##so it should be something.txt.xml
cd ../$1
for mytx in $(ls *.txt.xml); do mv $mytx ${mytx/.txt/} ; done
## something.txt.xml changed to something.xml
cd ..

for myt in $(ls $1/*.txt) ; do java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" -outputFormatOptions "CCPropagatedDependencies" $scriptdir/stanford-parser-2012-01-06/grammar/englishPCFG.ser.gz $myt > ${myt/.txt/.penn} ; done

for myp in $(ls $1/*.penn) ; do java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $myp -conllx -CCprocessed > ${myp/.penn/.LKconll} ; done

# So after all that, we should have, say: myinput.conll, myinput.txt, myinput.xml, myinput.penn, myinput.LKconll
# And finally, we want to get myinput.lemma_conll:

for mylkc in $(ls $1/*.LKconll) ; do python lemmatize_conll.py $mylkc ; done
