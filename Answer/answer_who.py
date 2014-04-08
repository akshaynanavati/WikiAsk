import nltk

def sublist_exists(sub, large):
    for item in sub:
        if item not in large:
            return False
    return True

def search_tree(tree, person, verb):
    if hasattr(tree, "node") and tree.node:
        for child in tree:
            result = search_tree(child, person, verb)
            if result:
                return result
        if sublist_exists(person, tree.leaves()) and verb in tree.leaves():
            return ' '.join(tree.leaves())
    return None

def get_definition(person, verb, sent):
    # need to check corefs
    # check for verb fail
    # check multiple names part
    if "PERSON" in sent.nes and person[0] in sent.nes["PERSON"]:
        if verb in sent.lemmas:
            verb = sent.lemmas.index(verb)
            verb = sent.words[verb]
            return search_tree(sent.parsetree, person, verb)          
    return None

def search_np(tree, name):
    if hasattr(tree, "node") and tree.node:
        if (tree.node in ["NP", "NN", "NNS", "NNP", "NNPS"] and
            name in tree.leaves()):
            return ' '.join(tree.leaves())
        for child in tree:
            search_np(tree, name)
    return None

def get_person(action, sent):
    for depend in sent.depends:
        if depend[0] == "nsubj":
            sent_action = depend[2]
            if sent.lemmas[sent.words.index(sent_action)] == action:
                name = depend[1]
                return search_np(sent.parsetree, name)
    return None

def get_who(sent, parsed_quest):
    for depend in parsed_quest.depends:
        if depend[0] == "nsubj" and depend[1].lower() == "who":
            name = [depend[2]]
            for d in parsed_quest.depends:
                if d[0] == "nn" and d[1] == name:
                    name.append(d[2])
            for d in parsed_quest.depends:
                if d[0] == "cop" and d[1].lower() == "who":
                    verb = parsed_quest.words.index(d[2])
                    verb = parsed_quest.lemmas[verb]
                    return get_definition(name, verb, sent)
                    
        elif depend[0] == "nsubj" and depend[2].lower() == "who":
            action = parsed_quest.words.index(depend[1])
            action = parsed_quest.lemmas[action]
            return get_person(action, sent)
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
        if not parsed_quest:
            return None
        answer = get_who(sent, parsed_quest)
        if answer:
            return answer
    return None
