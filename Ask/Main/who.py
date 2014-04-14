import sys, nltk

import lib

def generate_plural(npvp):
    pruned = npvp # lib.prune(npvp, "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["Whose"] + leaves[1:]

def generate(npvp):
    pruned = nltk.tree.Tree("S", npvp[1:]) # lib.prune(nltk.tree.Tree("S", npvp[1:]), "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["Who"] + [leaves[0].lower()] + leaves[1:]
