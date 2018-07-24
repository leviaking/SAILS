#!/usr/bin/env bash

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi

scriptdir=`dirname $0`

##LK: I need to compare two WSJ conll files. "A" is the original constituency parsed (.penn) file converted to a .conll file using Stanford. "B" is the same text, constituency parsed from plain text with Stanford, then converted to .conll using the same Stanford conversion command from above. Basically, "Does the initial constituency parse command (and parameters) change the constituency parse from its initial form?"
#
#pennfile=$1
#
#java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $pennfile -conllx -CCprocessed > ${pennfile/.penn/.conll_from_penn} 
#
#
#python conll_to_plain_text.py ${pennfile/.penn/.conll_from_penn} > "${pennfile/.penn/.txt}"
#
#### STOP HERE.
#
#### START AGAIN HERE.
#

textfile=$1

cd stanford-corenlp-full-2014-06-16
java -mx500m -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file $textfile -outputDirectory ..
##That should result in file $1.xml (i.e., something.txt.xml)
cd ..

java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" -outputFormatOptions "CCPropagatedDependencies" $scriptdir/stanford-parser-2012-01-06/grammar/englishPCFG.ser.gz $textfile > ${textfile/.txt/.parsed_penn}

java -mx800m -cp "$scriptdir/stanford-parser-2012-01-06/stanford-parser.jar:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile ${textfile/.txt/.parsed_penn} -conllx -CCprocessed > ${textfile/.txt/.parsed_conll}

# So after all that, we should have, say: myinput.conll, myinput.txt, myinput.xml, myinput.penn, myinput.LKconll
# And finally, we want to get myinput.lemma_conll:

#python lemmatize_conll.py ${1/.conll/.txt}
