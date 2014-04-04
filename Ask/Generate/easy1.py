# easy1.py
# author : Akshay Nanavati
#
# implements a basic algorithm for generating easy
# yes no questions by finding sentences of the form
# X [is | was] Y -> [is | was] X y?

import sys

sys.path.append("../")

import random, string, nltk, en

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

def find_index(npvp, tag):
    """
    Given a subtree with NPVP as the two nodes, we walk through it and 
    if the tag exists we return its index. Else return len(npvp).
    """
    firstnp = False
    pos = []
    n = len(npvp[0].pos())
    for child in npvp:
        if (not firstnp) and (child.node == "NP"):
            firstnp = True
        else:
            pos += child.pos()
    for i in xrange(len(pos)):
        if pos[i][1] == tag:
            return i + n
    return len(npvp.pos())

def prune (t, tag):
    """
    given a tree, removes any subtree who's child's root is tag
    """
    newchildren = []
    for child in t:
        if type(child) == str:
            newchildren = newchildren + [child]
        elif child.node != tag:
            newchildren = newchildren + [prune(child, tag)]
    return nltk.tree.Tree(t.node, newchildren)

def generateImpl(t):
    npvp = find_NP_VP(t)
    if npvp == None:
        return "could not find np/vp pattern".split(" ")
    pruned = prune(npvp, "SBAR")
    cci = find_index(pruned, "CC")
    sbari = find_index(pruned, "SBAR")
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
        print "\n-----\n"
        print "could not find verb in:"
        print pruned
        print "\n-----\n"
        return "could not find verb".split(" ")
    # else
    try:
        present = en.verb.present(v)
        i = leaves.index(v)
        return ["did"] + leaves[:i] + [present] + leaves[i + 1:]
    except:
        return ("could not conjugate verb '" + v + "'").split(" ")
    #return ["could", "not", "find", "is/was/are"]

def generate(ts):
    return [generateImpl(t) for t in ts]
        
