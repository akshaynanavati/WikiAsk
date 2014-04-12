import nltk
from itertools import groupby

def answer_long(sent, parsed_quest):
    # Just gets the first one -- parsed by tree maybe?
    if "DURATION" in sent.nes:
        dur_func = lambda x: x.ner
        answers = []
        for k, g in groupby(sent.words, dur_func):
            if k == "DURATION":
                words = list(g)
                words = [x.raw for x in words]
                answers.append(' '.join(words))
        return answers[0]
    return None

def answer_many(sent, parsed_quest):
    # again, just returns first...
    if "NUMBER" in sent.nes:
        return sent.nes["NUMBER"].pop()
    for depend in sent.depends:
        if depend[0] == "num":
            return depend[2]
    return None

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

def answer_do(sent, parsed_quest):
    # Similar to 'who' questions
    # essentially how does noun verb
    # Needs some info about the question probs
    action = None
    noun = None
    onto = None
    for depend in parsed_quest.depends:
        if depend[0] == "nsubj" or depend[0] == "nsubjpass":
            action = parsed_quest.get_lemma(depend[1])
            noun = parsed_quest.get_lemma(depend[2])
        if depend[0] == "dobj" and depend[1] == action:
            onto = parsed_quest.get_lemma(depend[2])
    if ((action and sent.has_lemma(action)) and
        (noun and sent.has_lemma(noun)) and
        ((not onto) or sent.has_lemma(onto))):
        return search_tree(sent.parsetree, [action, noun, onto])
    return None

def answer_far(sent, parsed_quest):
    return None

def answer(quest, f, kind):
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        if not parsed_quest:
            return None
        if kind == "howdo":
            answer = answer_do(sent, parsed_quest)
        elif kind == "howfar":
            answer = answer_many(sent, parsed_quest)
        elif kind == "howlong":
            answer = answer_long(sent, parsed_quest)
        elif kind == "howmany":
            answer = answer_many(sent, parsed_quest)
        elif kind == "howmuch":
            answer = answer_many(sent, parsed_quest)
        if answer:
            return answer
    return None
