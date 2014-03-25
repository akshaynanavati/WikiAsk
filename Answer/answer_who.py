import MontyLingua
import nltk

def get_verb(preds, subject):
    """
    This function finds the verb in the tuple where the subject is matched
    """
    for pred in preds:
        pred = pred.split('"')[1::2]
        if pred[1] == subject:
            return pred[0]
    return None

def get_subject(preds, verb):
    """
    This function finds the subject in the tuple where the verb is matched
    """
    for pred in preds:
        pred = pred.split('"')[1::2]
        if pred[0] == verb:
            return pred[1]
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
        sent = ' '.join(sent)
        preds = ml.jist_predicates(sent)[0]
        answer = get_subject(preds, verb)
        if answer:
            print quest, answer
            return answer
    return None
