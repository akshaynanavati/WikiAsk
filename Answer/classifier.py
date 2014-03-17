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
        return "When"
    elif tokens[0] == "where":
        return "Where"
    elif tokens[0] == "why":
        return "Why"
    elif tokens[0] == "who":
        return "Who"
    elif False:
        return "WhoRole"
    elif tokens[0] == "how":
        if tokens[1] == "do" or tokens[1] == "did":
            return "HowDo"
        elif tokens[1] == "far":
            return "HowFar"
        elif tokens[1] == "long":
            return "HowLong"
        elif tokens[1] == "many":
            return "HowMany"
        elif tokens[1] == "much":
            return "HowMuch"
        elif tokens[1] == "many" and tokens[2] == "times":
            return "HowManyTimes"
        else:
            return "HowProp"
    elif tokens[0] == "what":
        if False:
            return "WhatEquiv"
        elif tokens[1] == "type" or tokens[1] == "kind":
            return "WhatType"
        elif False:
            return "WhatPrep"
        elif False:
            return "WhatRole"
        elif False:
            return "WhatTime"
        elif False:
            return "WhatMeas"
        return "What"
    return None

def classify(sentence):
    """
    This function is the main purpose of this class, and returns the class
    of the question, as well as the keywords.
    """
    tokens = nltk.word_tokenize(sentence)
    tokens = [x.lower() for x in tokens]
    question_class = question_classify(tokens)
    keywords = get_keywords(tokens, question_class)
    return question_class, keywords

if __name__ == '__main__':
    print classify("Who am I?")
