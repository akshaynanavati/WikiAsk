import nltk


def get_definition(person, sent):
    # check that the 'be' belongs to the right person
    if "be" in sent.lemmas:
        split = sent.words[sent.lemmas.index("be")]
        defin = sent.raw.split(split)[1:]
        return person + " " + split + ''.join(defin)
    else:
        print "none", sent.raw
        return None

def get_person(definition, sent):
    print "IN", definition, sent.depends
    for depend in sent.depends:
        if depend[0] == "nsubj" and depend[2] == definition:
            return depend[1]
    return None

def get_who(sent, parsed_quest):
    print sent.raw
    print parsed_quest.raw
    print sent.depends
    print parsed_quest.depends
    print sent.nes
    print parsed_quest.nes
    print "SPACE"
    if "PERSON" not in sent.nes:
        return None
    print "YE"

    for depend in parsed_quest.depends:
        if (depend[0] == "nsubj" and depend[1].lower() == "who"):
            if ("PERSON" in parsed_quest.nes and 
                depend[2] in parsed_quest.nes["PERSON"] and
                depend[2] in parsed_quest.nes["PERSON"]):
                return get_definition(depend[2], sent)
            else:
                return get_person(depend[2], sent)
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
        answer = get_who(sent, parsed_quest)
        if answer:
            print quest, answer
            return answer
    return None
