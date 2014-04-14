import nltk

def get_overlap(list1, list2):
    print type(list1), type(list2)
    if not isinstance(list1, list):
        list1 = list1.split()
    if not isinstance(list2, list):
        list2 = list2.split()
    overlap = [x for x in list1 if x in list2]
    print list1, "000", list2, "000", overlap
    return float(len(overlap))/len(list2)

def trim_tree(tree, sent, quest, goal):
    if hasattr(tree, "node") and tree.node:
        for child in tree:
            result = trim_tree(child, sent, quest, goal)
            if result:
                return result
        words = []
        for w in tree.leaves():
            if w in sent.corefs:
                words.append(sent.corefs[w])
            else:
                words.append(sent.get_lemma(w))
        if get_overlap(words, quest.raw) >= goal:
            return tree.leaves()
    return None

def answer_what(sent, parsed_quest):
    s = []
    for word in sent.words:
        if word.raw in sent.corefs:
            s.append(sent.corefs[word.raw])
        else:
            s.append(word.lemma)
    s = ' '.join(s)
    overlap = get_overlap(s, parsed_quest.raw)
    result = trim_tree(sent.parsetree, sent, parsed_quest, overlap * .8)
    final = []
    for word in result:
        if word in sent.corefs:
            final.append(sent.corefs[word])
        else:
            final.append(word)
    return ' '.join(final)

def answer(quest, f):
    """
    This function is used to answer the what question, given the 
    question as a complete setence and the finder object
    """
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        answer = answer_what(sent, parsed_quest)
        if answer:
            return answer
    return None

