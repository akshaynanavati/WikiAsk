import sys, nltk

import lib

def generate_plural(npvp):
    pruned = lib.prune(npvp, "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["whose"] + leaves[1:]

def generate(npvp):
    pruned = lib.prune(nltk.tree.Tree("S", npvp[1:]), "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["who"] + leaves
