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
f = finder.Finder(source_filename)
c = classifier.Classifier()
questions = read_questions(questions_filename)

for question in questions:
    print c.classify(question)
    continue
    
    question_class, keywords, frame = classifier.classify(question)
    answer = ""
    print question
    if question_class == "When":
        answer = find.search_when(keywords)
    elif question_class == "Who":
        answer = find.search_who(keywords)
    elif question_class == "Where":
        answer = find.search_where(keywords)
    print answer + ' ' + ' '.join(frame)
    print '\n'
