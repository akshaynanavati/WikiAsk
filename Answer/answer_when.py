import nltk

def get_phrases(tree, phrases):
    if hasattr(tree, "node") and tree.node:
        pps = []
        if tree.node in phrases:
            pps = [tree]
        for child in tree:
            pps.extend(get_phrases(child, phrases))
        return pps
    return []

def has_time(tree, nes):
    if hasattr(tree, "node") and tree.node:
        if len(tree) == 1 and tree[0] in nes:
            return True
        for child in tree:
            if has_time(child, nes):
                return True
    return False

def is_bad_phrase(phrase, nes):
    if not has_time(phrase, nes):
        return True
    return False

def get_when(sent, quest_tree):
    nes = []
    if "DATE" in sent.nes:
        nes += sent.nes["DATE"]
    if "DURATION" in sent.nes:
        nes += sent.nes["DURATION"]
    preps = get_phrases(sent.parsetree, ["PP"])
    preps = [x for x in preps if not is_bad_phrase(x, nes)]
    preps = [' '.join(x.leaves()) for x in preps]

    #Eliminate overlapping preps
    final_prep = []
    for prep in preps:
        copy = list(preps)
        copy.remove(prep)
        if not len([x for x in copy if prep in x]):
            final_prep.append(prep)
    return ' '.join(final_prep)

def answer(quest, f):
    tokens = nltk.word_tokenize(quest)
    parsed_quest = f.parse_sentence(quest)
    for sent in f.yield_search(tokens):
        answer = get_when(sent, parsed_quest.parsetree)
        if answer:
            print quest, answer
            return answer
    return None
