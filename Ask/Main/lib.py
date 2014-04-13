import nltk

DEBUG = False
PORT = 5557

def set_debug (db):
    global DEBUG
    DEBUG = db

def set_port(port):
    global PORT
    PORT = port

def pretty_print(s, delim = "\n-----\n"):
    if DEBUG:
        print delim
        print s
        print delim

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

def error (s):
    if DEBUG:
        return s.split(" ")
    return None

which_words = set(["this", "that", "these", "those"]) 
                   #"every", "any", "some", "each"])
