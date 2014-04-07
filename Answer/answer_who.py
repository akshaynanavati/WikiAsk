import MontyLingua
import nltk
from itertools import combinations

def get_verb(preds, subject):
    """
    This function finds the verb in the tuple where the subject is matched
    """
    for pred in preds:
        pred = pred.split('"')[1::2]
        if pred[1] == subject:
            return pred[0]
    return None

def get_subject(preds, verb, f):
    """
    This function finds the subject in the tuple where the verb is matched
    """
    candidates = []
    for pred in preds:
        pred = pred.split('"')[1::2]
        if pred[0] == verb:
            candidates.append(pred[1])

    if len(candidates) == 0:
        return None

    # Process known entities to find the correct / best one
    known = sorted(f.entities["PERSON"].items(), key = lambda x: x[1],
            reverse = True)
    best = []
    for candidate in candidates:
        for entity in known:
            if candidate in entity[0] or entity[0] in candidate:
                best.append(entity)
                continue
    if len(best):
        return sorted(best, key = lambda x: x[1], reverse = True)[0][0]
    return None

def get_definition(person, sent):
    if "be" in sent.lemmas:
        print sent.raw
        split = sent.words[sent.lemmas.index("be")]
        defin = sent.raw.split(split)[1]
        return person + " " + split + define
    else:
        print "none", sent.raw
        return None

def get_who(sent, parsed_quest):
    print parsed_quest.depends
    for depend in parsed_quest.depends:
        if depend[0] == "cop" and depend[1].lower() == "who":
            return get_definition(depend[2], sent)
        else:
            return None

def answer(quest, f):
    """
    This function is used to answer the who question, given the question
    as a complete sentence, the montylingua object, and the finder object
    """
    # Find the verb attached to 'who'
    #preds = ml.jist_predicates(quest)[0]

    # Search
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        answer = get_who(sent, parsed_quest)
        if answer:
            print quest, answer
            return answer
    return None
