import nltk

def sublist_exists(sub, large):
    for item in sub:
        if item not in large:
            return False
    return True

def search_tree(tree, to_match):
    if hasattr(tree, "node") and tree.node:
        for child in tree:
            result = search_tree(child, to_match)
            if result:
                return result
        if sublist_exists(to_match, tree.leaves()):
            return ' '.join(tree.leaves())
    return None

def search_sent(sent, keyword):
    word = None
    for w in sent.words:
        if w.lemma == keyword:
            word = w.raw
    if word:
        return search_tree(sent.parsetree, [word, "because"])
    return None

def get_why(sent, parsed_quest):
    keyword = None
    for depend in parsed_quest.depends:
        if depend[0] == "root":
            keyword = parsed_quest.get_lemma(depend[2])
    if keyword:
        return search_sent(sent, keyword)
    return None

def answer(quest, f):
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        if not parsed_quest:
            return None
        answer = get_why(sent, parsed_quest)
        if answer:
            return answer
    return None
