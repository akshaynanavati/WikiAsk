import nltk

def answer_long(sent, parsed_quest):
    # use timex built into corenlp
    if "DURATION" in sent.nes:
        return sent.nes["DURATION"][0]        
    return None

def answer_many(sent, parsed_quest):
    if "NUMBER" in sent.nes:
        for depend in sent.depends:
            if depend[0] == "amod" and depend[2] == "many":
                target_index = sent.words.index(depend[1])
                number_indices = []
                for i in xrange(len(sent.words)):
                    if sent.pos[i] == "CD":
                        number_indices.append(i)
                inds = [(x, abs(target_index - x)) for x in number_indices]
                ind = min(inds, key = lambda x: x[1])[0]
                return sent.words[ind]
    return None

def answer_do(sent, parsed_quest):
    return None

def answer_for(sent, parsed_quest):
    return None

def answer_much(sent, parsed_quest):
    return None

def answer(quest, f, kind):
    tokens = nltk.word_tokenize(quest)
    print "token", tokens
    for sent in f.yield_search(tokens):
        print "sent", sent.raw
        print sent.nes
        print '\n'
        continue
        parsed_quest = f.parse_sentence(quest)
        if kind == "howdo":
            answer = answer_do(sent, parsed_quest)
        elif kind == "howfar":
            answer = answer_far(sent, parsed_quest)
        elif kind == "howlong":
            answer = answer_long(sent, parsed_quest)
        elif kind == "howmany":
            answer = answer_many(sent, parsed_quest)
        elif kind == "howmuch":
            answer = answer_much(sent, parsed_quest)
        if answer:
            return answer
    return None
