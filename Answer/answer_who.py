import nltk

def sublist_exists(sub, large):
    for item in sub:
        if item not in large:
            return False
    return True

def has_person(tree, sent):
    if "PERSON" in sent.nes:
        for name in sent.nes["PERSON"]:
            if name in tree.leaves():
                return True
    return False

def search_tree(tree, to_match):
    if hasattr(tree, "node") and tree.node:
        for child in tree:
            result = search_tree(child, to_match)
            if result:
                return result
        if sublist_exists(to_match, tree.leaves()):
            return ' '.join(tree.leaves())
    return None

def get_definition(name, cop, sent):
    if sent.has_lemma(cop):
        cop = sent.get_word(cop)
        return search_tree(sent.parsetree, [name, cop])
    return None

def get_person(action, sent):
    for depend in sent.depends:
        # match the action
        if depend[0] == "nsubj" or depend[0] == "nsubjpass":
            verb = depend[1]
            verb_lemma = sent.get_lemma(verb)
            if verb_lemma == action:
                name = depend[2]
                result = search_tree(sent.parsetree, [name, verb])
                if result and name in sent.corefs:
                    real_name = sent.corefs[name]
                    co_from = " %s " % name
                    co_to = " %s " % real_name
                    return result.replace(co_from, co_to)
                return result
    return None

def get_who(sent, parsed_quest):
    # Get dependencies
    # FUTURE - use 'nn' tag to get multiple parts of the name
    # ie ('nn', 'Dempsey', 'Jennifer')
    name = None
    cop = None
    action = None
    for depend in parsed_quest.depends:
        if depend[0] == "nsubj" and depend[1].lower() == "who":
            name = [depend[2]]
        elif depend[0] == "cop" and depend[1].lower() == "who":
            cop = parsed_quest.get_lemma(depend[2])
        elif depend[0] == "nsubj" and depend[2].lower() == "who":
            action = parsed_quest.get_lemma(depend[1])
        elif depend[0] == "nsubjpass" and depend[2].lower() == "who":
            action = parsed_quest.get_lemma(depend[1])
    if (name and cop):
        return get_definition(name, cop, sent)
    elif action:
        return get_person(action, sent)
    else:
        print parsed_quest.depends
        print "Could not find key words in: %s" % parsed_quest.raw
    return None

def answer(quest, f):
    """
    This function is used to answer the who question, given the question
    as a complete sentence, the montylingua object, and the finder object
    """
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        if not parsed_quest:
            return None
        answer = get_who(sent, parsed_quest)
        if answer:
            return answer
    return None
