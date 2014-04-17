#!/usr/bin/env python

import classifier
import finder
import sys
import os
import nltk

import answer_who
import answer_where
import answer_when
import answer_yesno
import answer_how
import answer_why
import answer_what

def read_questions(questions_filename):
    questions = []
    with open(questions_filename, 'r') as inputfile:
        for line in inputfile:
            questions.append(line[:-1])
    return questions      

source_filename = sys.argv[1]
questions_filename = sys.argv[2]

# Copy over the text and make it ascii-only characters.
# Put into a new directory for the Stanford batch parsing
if not os.path.isdir("texttemp/"):
    os.mkdir("texttemp/")
with open(source_filename, 'r') as inputfile:
    with open("texttemp/text", 'w') as output:
        for line in inputfile.readlines():
            text = line.decode("ascii", errors = "ignore")
            output.write(text)
try:
    f = finder.Finder("texttemp/")
except:
    try:
        with open(source_filename, 'r') as inputfile:
            with open("texttemp/text", 'w') as output:
                for line in inputfile.readlines():
                    sents = nltk.sent_tokenize(line)
                    for sent in sents:
                        text = sent.decode("ascii", errors = "ignore")
                        if len(text) == len(sent):
                            output.write(text)
                    output.write('\n')
        f = finder.Finder("texttemp/")
    except:
        f = finder.Finder(source_filename, True)

c = classifier.Classifier(f)
questions = read_questions(questions_filename)

for question in questions:
    wh_word = c.classify(question)
    
    answer = None
    if wh_word == "who":
        answer = answer_who.answer(question, f)
    elif wh_word == "where":
        answer = answer_where.answer(question, f)
    elif wh_word == "when":
        answer = answer_when.answer(question, f)
    elif wh_word == "yesno":
        answer = answer_yesno.answer(question, f)
    elif (wh_word == "howmany" or wh_word == "howlong" or 
        wh_word == "howdo" or wh_word == "howmuch" or wh_word == "howfar"):
        answer = answer_how.answer(question, f, wh_word)
    elif wh_word == "why":
        answer = answer_why.answer(question, f)
    elif wh_word == "what":
        answer = answer_what.answer(question, f)

    if answer:
        print answer
    else:
        # Last ditch effort .... just return the best sentence.
        tokens = nltk.word_tokenize(question)
        sent = next(f.yield_search(tokens))
        print sent.raw
