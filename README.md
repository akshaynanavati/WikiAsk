WikiAsk
=======

A program to generate and answer questions based on wikipedia articles for our NLP class at CMU



Before you start
----------------
Activate the virtual environment, which can be found at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/

If you're in a C shell, run:

source bootstrapenv/bin/activate.csh

Otherwise, if you're in a bash shell, run:

source bootstrapenv/bin/activate

You will know you're on the virtual environment if your prompt changes as such:

user$ -> (bootstrapenv)user$

You then need to add the nltk data path to your environment. This can be done
one of two ways. If you're using a C shell, then run:

setenv NLTK_DATA /afs/andrew.cmu.edu/usr3/pmassey/Public/project/ntlk_data/

Otherwise if you're on a bash shell, then run:

export NLTK_DATA=/afs/andrew.cmu.edu/usr3/pmassey/Public/project/nltk_data/



Question Generation
-------------------
To run our question generation script, you must be in a bash shell and you
must be located in the Ask/Main/ directory, located at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/WikiAsk/Ask/Main/

To run the script:

python ask.py <source article> <n>



Question Answering
------------------
To run our question answering script, you must be located in the Answer/
directory, located at
/afs/andrew.cmu.edu/usr3/pmassey/Public/project/WikiAsk/Answer/

To run the script:

python answer.py <source article> <questions>
