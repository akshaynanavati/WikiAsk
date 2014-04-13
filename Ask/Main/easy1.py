import sys

import random, string, nltk, en, lib

def generate(npvp):
    pruned = lib.prune(npvp, "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    verb = pruned[1][0]
    assert("V" == verb.node[0]) # verb tags start with V
    v = verb.leaves()[0]
    if v == "was":
        i = leaves.index("was")
        return [leaves[i]] + leaves[:i] + leaves[i + 1:]
    elif v == "is":
        i = leaves.index("is")
        return [leaves[i]] + leaves[:i] + leaves[i + 1:]
    elif v == "are":
        i = leaves.index("are")
        return [leaves[i]] + leaves[:i] + leaves[i + 1:]
    elif v == "":
        lib.pretty_print("could not find verb in:\n" + pruned)
        return lib.error("could not find verb")
    # else
    try:
        present = en.verb.present(v)
        i = leaves.index(v)
        return ["did"] + leaves[:i] + [present] + leaves[i + 1:]
    except:
        lib.error("could not conjugate verb '" + v + "'")
    #return ["could", "not", "find", "is/was/are"]
        
