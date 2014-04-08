import nltk

def get_phrases(tree, phrases):
    if hasattr(tree,"node") and tree.node:
        pps = []
        if tree.node in phrases:
            pps = [tree]
        for child in tree:
            pps.extend(get_phrases(child, phrases))
        return pps
    return []

def is_bad_phrase(prep, quest_tree, nes):
    # Elimiate phrases with a noun from the question
    prep_nouns = get_phrases(prep, ["NP"])
    prep_nouns = [' '.join(x.leaves()) for x in prep_nouns]
    quest_nouns = get_phrases(quest_tree, ["NP"])
    other_nouns = [[word for word, pos in x.pos() if pos in ["NP", "NN", "NNS", "NNP", "NNPS"]] for x in quest_nouns]
    quest_nouns = [' '.join(x.leaves()) for x in quest_nouns]
    other_nouns = [' '.join(x) for x in other_nouns]
    quest_nouns.extend(other_nouns)
    for noun in prep_nouns:
        for quest_noun in quest_nouns:
            if noun in quest_noun or quest_noun in noun:
                return True
    return False

def get_location(sent, quest_tree):
    if "LOCATION" in sent.nes:
        preps = get_phrases(sent.parsetree, ["PP"])
        preps = [x for x in preps if not is_bad_phrase(x, quest_tree, 
                sent.nes)]
        preps = [' '.join(x.leaves()) for x in preps]

        # Eliminate overlapping preps
        final_prep = []
        for prep in preps:
            copy = list(preps)
            copy.remove(prep)
            if not len([x for x in copy if prep in x]):
                final_prep.append(prep)
        return ' '.join(final_prep)
    return None

def answer(quest, f):
    # Search
    tokens = nltk.word_tokenize(quest)
    parsed_quest = f.parse_sentence(quest)
    if not parsed_quest:
        return None
    for sent in f.yield_search(tokens):
        answer = get_location(sent, parsed_quest.parsetree)
        if answer:
            return answer
    return None

