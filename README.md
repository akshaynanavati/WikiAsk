WikiAsk
=======

A program to generate and answer questions based on wikipedia articles for our NLP class at CMU



Before you start
----------------
If you are in a bash shell (recommended; to switch into one just 
run `/bin/bash`), simply run `source setup.sh` and skip the rest
of this section.

If you are in a C shell:

Activate the virtual environment, which can be found at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/ by:

source ../bootstrapenv/bin/activate.csh

You will know you're on the virtual environment if your prompt changes as such:

user$ -> (bootstrapenv)user$

You then need to add the nltk data path to your environment. This can be done
one of two ways. If you're using a C shell, then run:

setenv NLTK_DATA /afs/andrew.cmu.edu/usr3/pmassey/Public/project/ntlk_data/

Question Generation
-------------------
To run our question generation script, you must be in a bash shell and you
must be located in the Ask/Main/ directory, located at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/WikiAsk/Ask/Main/

To run the script:

`./ask.py <source article> <n>`

Question Answering
------------------
To run our question answering script, you must be located in the Answer/
directory, located at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/WikiAsk/Answer/

To run the script:

`./answer.py <source article> <questions>`

Sources
-------------------

Here are the external libraries and tools we used in this project:
  - http://www.nltk.org/book/ along with the NLTK library
  - http://nodebox.net/code/index.php/Linguistics for verb parsing
  - http://www.ark.cs.cmu.edu/mheilman/questions/ - specifically Java parse server
  - http://nlp.stanford.edu/software/corenlp.shtml - sentence parsing (server described above)
  - http://en.wikipedia.org/wiki/Okapi_BM25 - overall information retrieval algorithm
  - http://trec.nist.gov/pubs/trec9/papers/msrc-qa.pdf - ideas for overall implementation
  - http://nlp.stanford.edu/software/corenlp.shtml - StanfordCoreNLP, very useful text processing API
  - https://pypi.python.org/pypi/corenlp-python/3.2.0-3 - beginnings of communication with StanfordCoreNLP
  - http://nlp.stanford.edu/software/dependencies_manual.pdf - manual for dependencies
  - http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish - decorator for StanfordCoreNLP Timing
~                   
