# main.py
# author: Akshay Nanavati
# 
# the top level entrypoint for the ask program

import sys, os, string, subprocess, nltk

sys.path.append("../Parse")
sys.path.append("../Generate")

import parse
import easy1
import easy2
import generate

#print "starting parse server..."
#subprocess.call("./runStanfordParserServer.sh", shell=True)
#print "started"

# add other generation functions to this list
generate.register_generation([
    easy1.generate
    ])

fname = sys.argv[1]
nquestions = int(sys.argv[2])

f = open(fname)
article = f.readline()
f.close()

parsed = parse.parse(article)
for p in parsed:
    print p
    print "\n-----\n"

for q in generate.generate(parsed, nquestions)[0]:
    print q
    print "\n-----\n"
