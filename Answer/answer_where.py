import nltk
from stat_parser import Parser

def get_phrases(tree, phrase):
    if hasattr(tree,"node") and tree.node:
        if tree.node == phrase:
            return [tree]
        else:
            pps = []
            for child in tree:
                pps.extend(get_phrases(child, phrase))
        return pps
    return []

def is_bad_phrase(prep, quest_tree):
    prep_nouns = get_phrases(prep, "NP")
    quest_nouns = get_phrases(quest_tree, "NP")
    quest_nouns = [' '.join(x.leaves()) for x in quest_nouns]
    for noun in prep_nouns:
        noun = ' '.join(noun.leaves())
        for quest_noun in quest_nouns:
            if noun in quest_noun or quest_noun in noun:
                return True
    return False

def get_location(sent, quest_tree):
    if len(sent.nes["LOCATION"]) > 0:
        preps = get_phrases(sent.parsetree, "PP")
        preps = [x for x in preps if not is_bad_phrase(x, quest_tree)]
        preps = [' '.join(x.leaves()) for x in preps]
        return ' '.join(preps)
    return None

def answer(quest, ml, f):
    # Search
    tokens = nltk.word_tokenize(quest)
    parsed_quest = f.parse_sentence(quest)
    for sent in f.yield_search(tokens):
        answer = get_location(sent, parsed_quest.parsetree)
        if answer:
            print quest, answer
            return answer
    return None

