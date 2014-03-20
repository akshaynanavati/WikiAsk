import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import PlaintextCorpusReader

def get_keywords(tokens, question_class):
    accepted_tags = ["ADJ", "ADV", "FW", "N", "NP", "NUM", "PRO", "P", "UH",
            "V", "VD", "VG", "VN"]
    tags = nltk.pos_tag(tokens)
    tags = [(word, simplify_wsj_tag(tag)) for (word, tag) in tags]
    keywords = []
    for pair in tags:
        if pair[1] in accepted_tags:
            keywords.append(pair[0])
    return keywords

def question_classify(tokens):
    if tokens[0] == "when":
        return "When", tokens[1:]
    elif tokens[0] == "where":
        return "Where", tokens[1:]
    elif tokens[0] == "why":
        return "Why", None
    elif tokens[0] == "who":
        return "Who", tokens[1:]
    elif False:
        return "WhoRole", None
    elif tokens[0] == "how":
        if tokens[1] == "do" or tokens[1] == "did":
            return "HowDo", None
        elif tokens[1] == "far":
            return "HowFar", None
        elif tokens[1] == "long":
            return "HowLong", None
        elif tokens[1] == "many":
            return "HowMany", None
        elif tokens[1] == "much":
            return "HowMuch", None
        elif tokens[1] == "many" and tokens[2] == "times":
            return "HowManyTimes", None
        else:
            return "HowProp", None
    elif tokens[0] == "what":
        if False:
            return "WhatEquiv", None
        elif tokens[1] == "type" or tokens[1] == "kind":
            return "WhatType", None
        elif False:
            return "WhatPrep", None
        elif False:
            return "WhatRole", None
        elif False:
            return "WhatTime", None
        elif False:
            return "WhatMeas", None
        return "What", None
    return None, None

def classify(sentence):
    """
    This function is the main purpose of this class, and returns the class
    of the question, as well as the keywords.
    """
    tokens = nltk.word_tokenize(sentence)
    tokens = [x.lower() for x in tokens]
    question_class, frame = question_classify(tokens)
    keywords = get_keywords(tokens, question_class)
    return question_class, keywords, frame

if __name__ == '__main__':
    print classify("Who am I?")
