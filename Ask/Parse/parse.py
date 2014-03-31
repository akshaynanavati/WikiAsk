# parse.py
# author: Akshay Nanavati
#
# implements a basic parser for wiki articles.
# right now all it does is returun a line by line list of the file
# contents (where each line is a space seperated list of strings. 
# we probably will want a better parser later

import subprocess, socket, nltk

def parse_sentence(sentence):
    host = socket.gethostname()
    port = 5557
    s = socket.socket()
    s.connect((host, port))
    s.send(sentence + "\n")
    data = ""
    while (len(data) == 0) or (data[-1] != "\n"):
        data += s.recv(1024)
    ret = data.split("\n")[0]
    t = nltk.tree.Tree(ret)
    return t

def parse(text):
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return [parse_sentence(s) for s in tokenizer.tokenize(text)]
