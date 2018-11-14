# venkataraman-syllables

This is a python reimplementation of the maximum-likelihood estimation approach proposed by Anand Venkataraman for unsupervised word segmentation, but *uses syllables instead of phonemes*.

The paper describing the approach can be found at the link [here](http://www.aclweb.org/anthology/J01-3002)

To run, clone the repo:
```
git clone https://github.com/yczeng/venkataraman-approach.git
```
cd into the directory, and run:
```
python search.py
```
The results of the segmentation will be stored in `results/result.txt`.

## Scoring
Performance is measured using precision, recall, and F-score.

Precision is the number of correct words found out of all words found, recall is the number of correct words found out of all correct words, and F-scores it he geometric average of precision and recall (2 * precision * recall) / (precision + recall).

To score a segmented lexicon, run `score.py [segmented lexicon] [model lexicon]` where segmented lexicon and model lexicon are text files containing a dictionary of words in the lexicon. An example command is:

`python score.py results/lexicon.txt data/new.mother.speech-lexicon.txt` 

It looks like results for running the algorithm on syllables are:
```
Precision: 0.21204527081649152
Recall: 0.5918321299638989
f1 Score: 0.31222473515057736
```