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

def answer(quest, ml, f):
    """
    This function is used to answer the who question, given the question
    as a complete sentence, the montylingua object, and the finder object
    """
    # Find the verb attached to 'who'
    preds = ml.jist_predicates(quest)[0]
    verb = get_verb(preds, "who")
    if not verb:
        verb = get_verb(preds, "Who")
    if not verb:
        verb = get_verb(preds, "")
    if not verb:
        print "Failed to find verb that corresponds to 'who'"
        return None

    # Search
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        return sent
        preds = ml.jist_predicates(sent)[0]
        answer = get_subject(preds, verb, f)
        if answer:
            print quest, answer
            return answer
    return None
