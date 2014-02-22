# easy1.py
# author : Akshay Nanavati
#
# implements a basic algorithm for generating easy
# yes no questions by finding sentences of the form
# X [is | was] Y -> [is | was] X y?

import random, string

def swap(sent):
    for i in xrange(len(sent)):
        if sent[i] == "was" or sent[i] == "is":
            break
    return string.join([sent[i]] + sent[:i] + sent[i + 1:], " ")

def generate(wiki):
    def filterf(l):
        if "was" in l and "is" in l:
            return False
        else:
            return "was" in l or "is" in l
    was_is = filter(filterf, wiki)
    sent = was_is[random.randint(0, len(was_is) - 1)]
    return swap(sent)
