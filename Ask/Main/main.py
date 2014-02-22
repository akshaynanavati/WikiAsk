# main.py
# author: Akshay Nanavati
# 
# the top level entrypoint for the ask program

import sys, os, string

sys.path.append("../Parse")
sys.path.append("../Generate")

import parse
import easy1
import generate

# add other generation functions to this list
generate.register_generation([
    easy1.generate
    ])

fname = sys.argv[1]
nquestions = int(sys.argv[2])

wiki = parse.parse(fname)
print string.join(generate.generate(wiki, nquestions), "\n")
