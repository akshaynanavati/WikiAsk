import nltk
from stat_parser import Parser

def get_prep(tree):
    if hasattr(tree,"node") and tree.node:
        if tree.node == "PP":
            return [tree.flatten()]
        else:
            pps = []
            for child in tree:
                pps.extend(get_prep(child))
        return pps
    return []

def get_location(sent, f):
    p = Parser()
    print sent.nes
    if len(sent.nes["LOCATION"]) > 0:
        tree = p.parse(sent.raw)
        preps = get_prep(tree)
        preps = [' '.join(x.leaves()) for x in preps]
        return ' '.join(preps)
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

