import sys, os, string, subprocess, nltk

import parse
import easy1
import which
import who
import generate
import lib

#print "starting parse server..."
#subprocess.call("./runStanfordParserServer.sh", shell=True)
#print "started"

def main():
    # add other generation functions to this list
    generate.register_generation({
        "basic" : easy1.generate,
        "who" : who.generate,
        "whose" : who.generate_plural,
        "which" : which.generate
        })

    fname = sys.argv[1]
    nquestions = int(sys.argv[2])

    article = ""
    pars = 0

    f = open(fname)
    while pars <= 4: # take only first 4 paragraphs
        line = f.readline()
        if len(line) > 80:
            article += line
            pars += 1
    f.close()

    parsed = parse.parse(article)
    for p in parsed:
        lib.pretty_print(p)

    qs = generate.generate(parsed, nquestions)
    for q in qs:
        lib.pretty_print(q)

    while len(qs) < nquestions:
        qs += "could not generate question".split(" ")

    qs = qs[:nquestions]

    questions = map (lambda l: string.join(l, " "), qs)
    for q in questions:
        print q

