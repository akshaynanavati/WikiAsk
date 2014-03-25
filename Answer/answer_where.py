import nltk
import dateutil.parser
import datetime

def answer(quest, ml, f):
    # Search
    tokens = nltk.word_tokenize(quest)
    default = datetime.datetime(-1, -1, -1, -1, -1, -1)
    for sent in f.yield_search(tokens):
        sent = ' '.join(sent)
        try:
            date = dateutil.parser.parse(sent, fuzzy = True)
            
        except:
            continue

