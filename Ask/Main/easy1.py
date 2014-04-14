import sys

import random, string, nltk, en, lib

def generate(npvp):
    pruned = npvp # lib.prune(npvp, "SBAR")

    # capitalize first word or not?
    def ident(x):
        return x
    def lower(x):
        return x.lower()
    capitalize = ident
    if pruned.pos()[0][1] != "NNP":
        capitalize = lower

    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    verb = pruned[1][0]
    if ("V" != verb.node[0]): # verb tags start with V
        return lib.error("'" + verb.node[0] + "' is not a known verb tag")
    v = verb.leaves()[0]
    if v == "was":
        i = leaves.index("was")
        return [leaves[i].capitalize()] + [capitalize(leaves[0])] + leaves[1:i] + leaves[i + 1:]
    elif v == "is":
        i = leaves.index("is")
        return [leaves[i].capitalize()] + [capitalize(leaves[0])] + leaves[1:i] + leaves[i + 1:]
    elif v == "are":
        i = leaves.index("are")
        return [leaves[i].capitalize()] + [capitalize(leaves[0])] + leaves[1:i] + leaves[i + 1:]
    elif v == "":
        return lib.error("could not find verb")
    # else
    try:
        negate = []
        if random.randint(0, 1) == 0:
            negate = ["not"]
        present = en.verb.present(v)
        i = leaves.index(v)
        return ["Did"] + [capitalize(leaves[0])] + leaves[1:i] + negate + [present] + leaves[i + 1:]
    except:
        return lib.error("could not conjugate verb '" + v + "'")        
