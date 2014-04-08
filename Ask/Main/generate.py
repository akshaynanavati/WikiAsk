# generate.py
# author: Akshay Nanavati
#
# generates n questions based on a wikipedia article

import random, nltk, lib

gens = {}
MAX_TRY = 10

class AlgError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def register_generation(fs):
    global gens
    for k in fs:
        gens[k] = fs[k]

def find_NP_VP(t):
    """
    This will return a subtree with the node S and two subnodes NP and VP.
    """
    npi = -1
    for child in t:
        if type(child) == str:
            return None
        if (child.node == "S") and (len(child) >= 2):
            for i in xrange(len(child)):
                if child[i].node == "NP":
                    npi = i
                if (npi >= 0) and (npi == (i - 1)) and child[i].node == "VP":
                    return nltk.tree.Tree("S", [child[npi], child[i]])
        return find_NP_VP(child)
    return None

def is_subject_prp(npvp):
    """
    given a tree in npvp form, returns true if the nnp portion
    of the sentence is a PRP (personal pronoun)
    """
    np = npvp[0]
    return np[0].node == "PRP"

def is_subject_plural_pp(npvp):
    """
    given a tree in npvp form, returns true if the nnp portion
    of the sentence is a PRP (personal pronoun)
    """
    np = npvp[0]
    return (type(np[0][0]) != str) and (np[0][0].node == "PRP$")

def is_subject_dt(npvp):
    np = npvp[0]
    return (np[0].node == "DT") and (np[0][0].lower() in lib.which_words)

def generate(wiki, n):
    """
    given a list of parsed sentences as parse trees, generates
    1 question based on that sentence.
    """
    def gen (sent):
        npvp = find_NP_VP(sent)
        if npvp == None:
            return "could not find np/vp pattern".split(" ")
        if is_subject_prp(npvp):
            return gens["who"](npvp)
        elif is_subject_plural_pp(npvp):
            return gens["whose"](npvp)
        elif is_subject_dt(npvp):
            return gens["which"](npvp)
        # else
        return gens["basic"](npvp)
    return map(gen, wiki)

# random alg generation
def generate_(wiki, n):
    questions = []
    tries = 0
    if gens == []:
        raise AlgError ("no registered algorithm for question generation")
    while len(questions) < n and tries < MAX_TRY:
        algi = random.randint(0, len(gens) - 1)
        q = gens[algi](wiki)
        if q in questions:
            tries += 1
        else:
            questions += [q]
            tries = 0
    return questions
