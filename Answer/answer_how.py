import nltk
from itertools import groupby

def answer_long(sent, parsed_quest):
    # Just gets the first one -- parsed by tree maybe?
    if "DURATION" in sent.nes:
        dur_func = lambda x: x.ner
        answers = []
        for k, g in groupby(sent.words, dur_func):
            if k == "DURATION":
                words = list(g)
                words = [x.raw for x in words]
                answers.append(' '.join(words))
        return answers[0]
    return None

def answer_many(sent, parsed_quest):
    if "NUMBER" in sent.nes:
        return sent.nes["NUMBER"].pop()
    for depend in sent.depends:
        if depend[0] == "num":
            return depend[2]
    return None

def answer_do(sent, parsed_quest):
    return None

def answer_for(sent, parsed_quest):
    return None

def answer_much(sent, parsed_quest):
    return None

def answer(quest, f, kind):
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        if not parsed_quest:
            return None
        if kind == "howdo":
            answer = answer_do(sent, parsed_quest)
        elif kind == "howfar":
            answer = answer_far(sent, parsed_quest)
        elif kind == "howlong":
            answer = answer_long(sent, parsed_quest)
        elif kind == "howmany":
            answer = answer_many(sent, parsed_quest)
        elif kind == "howmuch":
            answer = answer_much(sent, parsed_quest)
        if answer:
            return answer
    return None
