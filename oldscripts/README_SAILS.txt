10/1/2015. LK.

LAST UPDATED: 04/21/2016.

*Technical Documentation.*

This document describes the steps performed in getting from plain text NS and NNS PDT responses to ranked NNS sentences and finally to rankings of the experiments that created the ranked NNS sentences.


*Preparing the tf-idf reference corpus (or corpora).*
At this point, we're using just two: the WSJ Corpus and the Brown Corpus, both from the PTB. They need to be reparsed to match our parsing parameters. The script conll_to_reparsed_to_lemmatized_conll.sh handles this: it operates on a directory of .conll files. For each conll file, it runs the conll_to_plain_text.py script, whih pulls out the plain text sentences and saves them as a .txt file. Note that conll_to_plain_text.py will skip over any sentences that contain more than one punctuation character in a row. (It's not ideal, but these are problematic.) Then it runs the Stanford CoreNLP lemmatizer on the text files, producing a .xml file containing the lemmatized sentence in Stanford's format. Then it runs the Stanford Parser, first generating a PTB style constituency parsed ".penn" file and then converting that to a dependency parsed file saved as .LKconll ("LK" being my initials and denoting that it's parsed with my parameters). Finally, the script runs the lemmatize_conll.py script, which takes the .LKconll file and replaces the words with the corresponding lemmas from the .xml file, resulting in  a .lemma_conll file. At this point, all the above files will be saved directly in the folder in which the .conll files began. From the "main/" directory, the command is:
./conll_to_reparsed_to_lemmatized_conll.sh wsj ##where "wsj" is the folder containing the .conll files.

To make this work, you'll need to have this directory setup:

main/
    conll_to_reparsed_to_lemmatized_conll.sh
    text_to_lemmatized_conll.sh
    conll_to_plain_text.py
    lemmatize_conll.py
    wsj/
        *.conll
        (*.txt)
        (*.xml)
        (*.penn)
        (*.LKconll)
        (*.lemma_conll)
    brown/
        (contents are same format as wsj/)
    stanford_parser/
        (stanford parser stuff)
    stanford_core_nlp/
        (stanford core nlp stuff)
----(below applies to "Preparing the NS & NNS data")-------
    text_to_lemmatized_conll.sh
    NS/
        *.txt
        (*.conll, etc. as above)
    NNSO/
        *.txt
        (*.conll, etc. as above)
    NNSLM/
        *.txt
        (*.conll, etc. as above)
----------------------------------
    prep_conll_for_tfidf.sh
    prep_conll_for_tfidf.py
    
Note that directory names of the two Stanford directories are hardcoded in the .sh script, so you'll need to check your version of the tools and modify the directory names in the .sh script accordingly.


*Preparing the NS & NNS data.*
Next we need to get .lemma_conll files for the NS and NNS sentences. (Remember that the NS responses for a given item are contained in one text file (one sentence per line), but each NNS response is in its own file (one sentence per FILE).) Note that we're using "NNSO" and "NNSLM" to refer to the original version and the LM-preferred version of the NNS data. For this, we use the script text_to_lemmatized_conll.sh. It's basically the same as conll_to_reparsed_to_lemmatized_conll.py, but does not include the intial steps involved in getting plain text from conll. This will result in files that correspond to those described above ("Preparing the tf-idf refernce corpus"). This is run with this command:
./text_to_lemmatized_conll.sh XYZ ##where "XYZ" is the directory containing the .txt files.


*Preparing dependency strings.*
We prepare "dependency strings" for tf-idf (and the for the baseline measures). These depstrings are concatenated strings of the form label_dep_head (in fact we use label$@%dep$@%head). We also use x_dep_head, label_x_head, label_dep_x and x_dep_x.
## As of 4/21/2016 and the BEA2016 paper, the statement immediately below is no longer true. We made some late changes to the paper and substituted the "xdx" depstrings in the place of true lemmas. The relevant scripts have not been updated to operate on true lemmas in a way that is consistent with the BEA2016 work. These files could likely be updated fairly easily if needed.
## (Additionally, we perform a more traditional tf-idf in which we use each lemmatized word from the sentence alone; i.e., not in a concatenated depstring. This simply operates on the .lemma_conll files, so it's not involved in this current step.)
This process is performed on the NS files, NNS files and reference corpora. (Note that we're starting with the Brown and WSJ data as distributed in the PTB; i.e., the files are split up just as they originally were, not concatenated or otherwise changed.) The script prep_conll_for_tfidf.sh derives files for these different depstring formats from the .lemma_conll files (by running prep_conll_for_tfidf.py on them). Each of these resulting files shares the name of the file from which it was derived, but replaces the .lemma_conll extension with one of: .ldh, .xdh, .lxh, .ldx, .xdx. After generating all the files, the shell script then creates a subfolder for each of these extensions (only those that don't already have a subfolder), and moves each of the files into its corresponding subfolder.
This is run with this command:
./prep_conll_for_tfidf.sh NNS ##where "NNS" (or "myref" or " is the directory containing the .lemma_conll files.

This should result in the following:

main/
    conll_to_reparsed_to_lemmatized_conll.sh
    text_to_lemmatized_conll.sh
    conll_to_plain_text.py
    lemmatize_conll.py
    wsj/
        conll/
        ldh/
        ldx/
        lemma_conll/
        LKconll/
        lxh/
        penn/
        txt/
        xdh/
        xml/
        txt/
        xml)
    brown/
        (contents are same format as wsj/)
    NS/
        (contents are same format as wsj/)
    NNSO/
        (contents are same format as wsj/)
    NNSLM/
        (contents are same format as wsj/)
    stanford_parser/
        (stanford parser stuff)
    stanford_core_nlp/
        (stanford core nlp stuff)
    text_to_lemmatized_conll.sh
    prep_conll_for_tfidf.sh
    prep_conll_for_tfidf.py
    

*Getting tf-idf scores for depstrings.*
With the data formatted for analysis, the next step is to get tf-idf scores for the depstrings (or bare lemmas) in the NS and NNS data. The scripts lk_tfidf.sh and lk_tfidf.py are used here.
The implementation of tf-idf is described in the BEA2016 paper. Here is an excerpt (in LaTeX form):

Calculating tf-idf relies on both \emph{term frequency} ($tf$) and
\emph{inverse document frequency} ($idf$).  Term frequency is simply
the raw count of an item, and for tf-idf of terms in the GS, we take
this as the frequency within the GS.  Inverse document frequency is
derived from some reference corpus, and it is based on the notion that
appearing in more documents makes a term less informative with respect
to distinguishing between documents.  The formula is in
(\ref{ex:tfidf}) for a term $t$, where $N$ is the number of documents
in the reference corpus, and $df_{t}$ is the number of documents
featuring the term ($idf_{t} = \log \frac{N}{df_{t}}$).  A term
appearing in fewer documents will thus obtain a higher $idf$ weight,
and this should readjust frequencies based on semantic importance.

\begin{exe}
  \ex\label{ex:tfidf} $tfidf(t) = tf_{GS} \log \frac{N}{df_{t}}$
\end{exe}

An example command for this process is:
./lk_tfidf.sh GS brown ##where "GS" is the test folder and "brown" is the reference folder.
This creates an output folder where the results will be stored. This folder is arg1 + '_' + arg2 + '_tfidf'; so in the example here, it's 'GS_brown_tfidf'.
It then iterates through each of the relevant files in the subfolders of the test folder. The shell script then runs the lk_tfidf.py script on the test file and the reference corpus. This python script basically just runs the tfidf function on the data and returns a list of terms and their scores, which the shell script then saves to a file in the results folder. These files are named according to the item number, participant number, depstring format and reference corpus. Here's an example for item 1, participant 39, label_dependent_head format, and wsj reference corpus: "i01p39.ldh_wsj.results".
This should result in the following additions to the "main" directory:

main/
    ...
    NNSO_brown_results/
        i01p01.ldx_brown.results
        ...
    NNSO_wsj_results/
        ...
    NNSLM_brown_results/
        ...
    NNSLM_wsj_results/
        ...
    ...


*Running the sentence ranking experiments.*
At this point, we're running four basic types of experiments. These combine 2 methods of weighting terms (tf-idf ("T") and frequency ("F")) with 2 methods for comparing the NNS and GS data (average ("A") means that each test (NNS) term receives a score that is simply the weight of the term *from the GS*; cosine ("C") means that for *both* the NNS and GS, terms were weighted (via tfidf or frequency), then we get the union set of GS and NNS terms, create a list of these terms' weights for the GS and another for the NNS, then treat these as vectors and calculate the cosine similarity). This yields the four methods: FA, TA, FC, TC.

So FA involves no tf-idf. Instead, this approach simply operates on the depstrings output by prep_conll_for_tfidf.py above. For a given PDT item, the baseline approach calculates the relative frequency of each depstring in the GS (the collection of NS responses). Then, for a test item (an NNS response), it takes the depstrings, looks for them in the GS and assigns them a score which is the relative frequency in the GS. Any depstrings not found in the GS get a score of 0, and the NNS response gets an overall score which is the average of these depstring scores. (FA can be seen as our baseline for this work.)
TA experiments are similar to the FA experiments, but in this case, rather than assigning a term in the test sentence a score which is the RF of the term in the GS, we instead assign it a score which is the tf-idf score taken directly from the GS. That is, we run tf-idf on the GS, and score the test sentence with the resulting tf-idf scores alone.
The FC approach involves weighting the terms in the GS according their relative frequency there, and doing the same for each test sentence. We then treat these as vectors and get a cosine similarity score for each test sentence. This means we first get the union set from the set of test sentence terms and the set of GS terms, because each will likely have one or more terms not seen in the other. The resulting sets and scores can then be compared as vectors.
The TC approach involves weighting the terms in the GS according their tfidf scores there, and doing the same for each test sentence. As in FC, we then treat these as vectors and get a cosine similarity score for each test sentence. 

All four of the above types of ranking experiments are run with sentence_rankings.py. The command is:
python sentence_rankings.py test_directory gold_directory
At this point, the script needs to be run four times to get full set of rankings; here are the commands:
python sentence_rankings.py NNSO_brown_tfidf GS_brown_tfidf
python sentence_rankings.py NNSO_wsj_tfidf GS_wsj_tfidf
python sentence_rankings.py NNSLM_brown_tfidf GS_brown_tfidf
python sentence_rankings.py NNSLM_wsj_tfidf GS_wsj_tfidf
(Note that the script has the locations of the GS, NNSO and NNSLM texts hardcoded, and a single execution of the script runs the full FA and FC experiments. So when we run the 4 commands above in order to get all the tfidf test+reference combinations, it actually performs FA and FC 4 times and simply overwrites it each time; no big deal for the small amount of data we're working with).
With our current parameters, this results in 60 different experiments, where each experiment is a combination of parameters resulting in a ranked list of the NNS responses for a single PDT item. With our 10 items, running the above commands generates 600 .csv files. These files are written to a folder called "exp_csv", which is created only if it doesn't already exist. Each of these csvs has 4 columns: score, sentence, semantic triple (from the 2013/2014 analysis), and error type (from the 2013/2014 analysis). These rows are sorted by the scores, from best to worst.
[Note that the four experiments FA, TA, FC, TC were originally known as B, A, C, M and then temporarily as FA, IA, FC, IC ("I" for importance score (a poor implementation of tf-idf that we abandoned after the initial BEA2016 submission, but before the final BEA2016 submission)).]

## The following is out of date. As of 4/21/2016 and as of the final BEA2016 paper, I have not updated the joint analysis script. If desired, this would probably not be more than a few hours of work.
## Because neither the NNSO (original) or the NNSLM (spelling correction/language model output) source always performs better than the other, we also perform a "joint" analysis. This means that for each NNSO sentence, we process the corresponding NNSLM sentence in parallel, then we choose one and discard the other, meaning only one of these two sentences makes it into the ranking. In this decision of which version to keep, we simply choose the one that has a "better" score (in the case of the RF baseline, this is the higher score; in the case of the "main" cosine approach, this is the smaller score). This results in 21 different rankings per item, and 210 total. This joint analysis is run with the joint_sentence_rankings.py script, which is a variation on the sentence_rankings.py script. The output goes into joint_csv, which is created only if it doesn't already exist. Each of these csvs has 5 columns: score, sentence, source (NNSO or NNSLM), semantic triple (from the 2013/2014 analysis), and error type (from the 2013/2014 analysis). These rows are sorted by the scores, from  best to worst. This script needs to be run twice to get the full set of joint rankings; here are the commands:
## python joint_sentence_rankings.py NNSO_wsj_results NNSLM_wsj_results GS_wsj_results
## python joint_sentence_rankings.py NNSO_brown_results NNSLM_brown_results GS_brown_results

4/21/2016 1:51 pm: CONTINUE UPDATING BELOW...

Ranking the experiments.
Each experiment results in a ranked list of sentences for each item. Because we have the manually annotated errors from our 2013/2014 papers, we can score each experiment according to how it ranked the sentences containing these errors. We rank sentences from worst to best (or least- to most-similar-to-the-GS) using the sentence ranking output from the previous step.
We used at least three different metrics for scroring the experiments. The primary metric is (Mean) Average Precision (MAP or AP, as appropriate). See the BEA2016 paper for a description of this metric and its implementation.
The script avg_prec_ranker.py is used to get the average precision scores for individual experiment settings, and then rank these. This results in a .csv file of AP rankings for each of the 10 PDT items, and an additional .csv of MAP rankings averaged across all 10 items. This output goes in the folder exp_avg_precision/. This script does not take any arguments (the files and paths are hardcoded).

## [The following discusses error_ranker.py and is not up to date. In the initial submission to BEA2016, we used something we called the "Normalized" metric, described below. In various places (scripts, etc.) I also referred to this as "distance":]
## Then each sentence containing an error is assigned a score equal to its rank, and these scores are summed to give us the experiment score. Thus the idea is that a good experiment is one that receives a low score overall, because the errors tend to be clustered near the top (i.e., at the top of the .csv rows) of the ranked sentences (or eliminated completely, becoming a "0", which is possible under the joint analysis). Then we can rank experiments according to these scores. This ranking is performed with the script error_ranker.py. This script operates on the csvs generated in the previous step, and takes no arguments, so the command is simply:
## python error_ranker.py.
## The output goes into exp_scores, which is created only if it doesn't already exist. For each of the 10 items, the script generates a ranking of experiments and their scores, stored as a csv. It also produces an overall ranking by averaging each experiment's score across the 10 items.
## [The following discussion of joint error ranking is also out of date]
## error_ranker.py operates specifically on the files in exp_csv; i.e., not on the joint analysis files. A modified version operates on the files in joint_csv; this is called joint_error_ranker.py; it also takes no arguments and its output goes into joint_scores.
## These two scripts (error_ranker.py and joint_error_ranker.py) do not include errors labeled "coverage" in their calculations (only "triple" and "form"). We wanted another experiment ranking where we include "coverage" errors, so we have the versions cov_error_ranker.py and cov_joint_error_ranker.py; these also take no arguments, and their output goes into cov_exp_scores and cov_joint_scores.


10/22/2016.
WordNet modifications. In April and May of 2016, I implemented a bare-bones attempt at expanding the GS with WordNet. Here's how it works:


Get as much of the pipeline as possible into shell scripts; play with WordNet and see what the old data does.



Second Language Aquisition
   Motivation: What works for learners and what doesn't
   What systems currently exist? What has been tried?

Computational Linguistics:
   Motivations/Principles ("low-resource"?)
   Gold Standard
      How to define a GS (NS responses? Elicited with what instructions?)
      Representation / modeling
      Native-like vs. accurate
   Data Collection
      PDTs (motivation, uses, design, variability, etc.)
      NS and NNS
      Should we "pilot" this as new module creation?
   Pre-processing
      Spelling correction
      Language modeling
         Training data
   Comparing NNS & NS/GS (experiments for developing system and evaluation scheme)
      Dependency parsing
         Training data
      Rule-based triple extraction (BEA2013)
      Dependency-based tf-idf
         Choosing reference corpora
         Compare GS vector and NNS vector (cosine)
         Score NNS using GS scores ("alpha")
         (Baseline: Score NNS using relative frequency of terms in GS)
      Lexical expansion/abstraction?
         WordNet?
         Abstract Meaning Representation?
      Other representations
         Semantic role labeling
         (AMR?)
   Evaluating NNS responses
      Feedback for learners

Product concerns
   New module creation (teachers/users can add content & crowdsource GS)
   Evolving gold standard (GS is reprocessed as new responses are added)
   Release
      How? Host this online?
      What resources would this require?
   Game elements
      Branching story trees?
         "Choose your own adventure"
         Adaptive testing
      Feedback


