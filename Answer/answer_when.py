import nltk
from collections import defaultdict

def get_time_or_date(sent, f):
    known = []
    if "DATE" in f.entities:
        known += f.entities["DATE"].items()
    if "TIME" in f.entities:
        known += f.entities["TIME"].items()
    known = sorted(known, key = lambda x: x[1], reverse = True)
    for entity in known:
        if entity[0] in sent:
            return entity[0]
    return None

def answer(quest, ml, f):
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        answer = get_time_or_date(sent, f)
        if answer:
            print quest, answer
            return answer
    return None
