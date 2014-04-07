import classifier
import finder
import sys

import answer_who
import answer_where
import answer_when
import answer_yesno

def read_questions(questions_filename):
    questions = []
    with open(questions_filename, 'r') as inputfile:
        for line in inputfile:
            questions.append(line[:-1])
    return questions      

source_filename = sys.argv[1]
questions_filename = sys.argv[2]

f = finder.Finder(source_filename)
c = classifier.Classifier(f)
questions = read_questions(questions_filename)

for question in questions:
    wh_word = c.classify(question)
    
    if wh_word == "who":
        answer_who.answer(question, f)
    elif wh_word == "where":
        answer_where.answer(question, f)
    elif wh_word == "when":
        answer_when.answer(question, f)
    elif wh_word == "yesno":
        answer_yesno.answer(question, f)
    else:
        print "Did not find that question a home."
