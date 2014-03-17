import classifier
import finder
import sys

def read_questions(questions_filename):
    questions = []
    with open(questions_filename, 'r') as inputfile:
        for line in inputfile:
            questions.append(line[:-1])
    return questions      

source_filename = sys.argv[1]
questions_filename = sys.argv[2]
find = finder.Finder(source_filename)
questions = read_questions(questions_filename)

for question in questions:
    question_class, keywords = classifier.classify(question)
    print question
    print find.search_who(keywords)
    print '\n'
