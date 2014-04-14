import sys, os, string, subprocess, nltk, random

import parse
import easy1
import which
import who
import generate
import lib

def main():
    # add other generation functions to this list
    generate.register_generation({
        "basic" : easy1.generate,
        "who" : who.generate,
        "whose" : who.generate_plural,
        "which" : which.generate#,
        })

    fname = sys.argv[1]
    nquestions = int(sys.argv[2])

    paras = []

    f = open(fname)
    line = f.readline()
    # take only real paragraphs, not titles or tables
    while line != "":
        if len(line) > 70:
            paras += [line]
        line = f.readline()
    f.close()

    all_qs = []
    qs = []

    while (len(qs) < nquestions) and (len(paras) > 0):
        i = random.randint(0, len(paras) - 1)
        p = paras.pop(i)
        parsed = parse.parse(p)
        all_qs += filter(lambda x: (type(x) == tuple) and 
                                   (x[0] != None) and 
                                   (lib.wc(x[0]) > 5),
                         generate.generate(parsed))
        flips = [random.randint(0, 2) for i in xrange(len(all_qs))]
        new_qs = []
        for i in xrange(len(flips)):
            if flips[i] == 0:
                qs += [all_qs[i][0]]
            else:
                new_qs += [all_qs[i]]
        all_qs = new_qs

    lib.pretty_print(qs)
    lib.pretty_print(all_qs)
    questions = map (lib.format, qs)
    for q in questions:
        print q

