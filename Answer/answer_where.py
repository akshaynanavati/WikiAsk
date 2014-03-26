import nltk

def get_location(sent, f):
    known = sorted(f.entities["LOCATION"].items(), key = lambda x: x[0],
            reverse = True)
    for entity in known:
        if entity[0] in sent:
            return entity[0]
    return None


def answer(quest, ml, f):
    # Search
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        answer = get_location(sent, f)
        if answer:
            print quest, answer
            return answer
    return None

