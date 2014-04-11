import nltk
from nltk.tag.stanford import NERTagger

from itertools import groupby
import math

import re
from corenlp import StanfordCoreNLP, batch_parse

import errno
import signal
import os
from functools import wraps

import os
import sys

class Word:
    def __init__(self):
        self.raw = ""
        self.lemma = ""
        self.pos = ""
        self.ner = ""

    def __repr__(self):
        return "%s - %s - %s - %s" % (self.raw, self.lemma, self.pos, 
                self.ner)

class Sentence:
    def __init__(self):
        self.raw = ""
        self.words = []
        self.corefs = {}
        self.parsetree = None
        self.depends = []
        self.nes = {}

    def get_searchable(self):
        coref_str = ' '.join(self.corefs.values())
        return self.raw + " " + coref_str

    def get_lemma(self, w):
        for word in self.words:
            if word.raw == w:
                return word.lemma
        return None

    def get_word(self, l):
        for word in self.words:
            if word.lemma == l:
                return word.raw
        return None

    def has_lemma(self, lemma):
        for word in self.words:
            if word.lemma == lemma:
                return True
        return False

class TimeoutError(Exception):
    pass

def timeout(seconds, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

class Finder:

    class Paragraph:
        def __init__(self):
            self.text = ""
            self.sents = []

    def __init__(self, filedir):
        #with open(filename, 'r') as inputfile:
        #    self.raw = inputfile.read()
        #paras = self.raw.split('\n\n')
        #self.paras = [x for x in paras if len(x) > 0]
        self.filedir = filedir
        self.corenlp = StanfordCoreNLP()
        self.batchcorenlp = batch_parse(filedir)
        self.sents = self.parse_document()
        #self.entities = self.get_entities(self.raw)

    def get_entities(self, text):
        """
        This function gets all entities for the article.
        """
        ner_tagger = NERTagger("stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz",
                "stanford-ner/stanford-ner.jar")
        entities = {}
        text = ''.join(x for x in text if x != '.')
        tags = ner_tagger.tag(text.split())
        # Merge Tags
        all_people = []
        for key, group in groupby(tags, lambda x: x[1]):
            if key != 'O':
                entity = ' '.join(x[0] for x in group)
                if key not in entities:
                    entities[key] = defaultdict(int)
                entities[key][entity] += 1
        return entities
    
    @timeout(10)
    def _parse(self, text):
        return self.corenlp.raw_parse(text)

    def is_ascii(self, text):
        try:
            text.encode("ascii")
        except:
            return False
        return True

    def lists_without(self, list1, missing):
        if missing == 0:
            return [list1]
        lists = []
        for i in xrange(len(list1)):
            here = list1[:i] + list1[i + 1:]
            lists.extend(self.lists_without(here, missing - 1))
        return lists

    def compare_str(self, str1, str2):
        # This function compares the str1 with the possibly unicode
        # containing str2. It removes all unicode words from str2 and then
        # compares the two strings.
        text2 = []
        missing = 0
        for word in str2.split():
            if self.is_ascii(word):
                text2.append(word)
            else:
                missing += 1
        text2 = ' '.join(text2) 
        text1 = str1.split()
        for sublist in self.lists_without(text1, missing):
            sub = ' '.join(sublist)
            if sub in text2:
                return True
        return False

    def get_parse(self, text):
        tries = 0
        parse = {"sentences" : []}
        while not parse["sentences"]:
            tries += 1
            if tries > 15:
                # not happenin', give up
                return None
            if tries > 8:
                # reset Stanford
                self.corenlp = StanfordCoreNLP()
            try:
                parse = self._parse(text)
            except Exception as error:
                continue
            # Assert it is this correct parsing
            for sent in parse["sentences"]:
                if self.compare_str(sent["text"], text):
                    return parse
            parse = {"sentences" : []}
            continue
        return None

    def parse_sentence(self, text):
        parse = self.get_parse(text)
        if not parse:
            return None
        sent = parse["sentences"][0]
        s = Sentence()
        s.raw = sent["text"]
        s.parsetree = nltk.Tree(sent["parsetree"])
        s.depends = sent["dependencies"]
        for w in sent["words"]:
            word = Word()
            word.raw = w[0]
            word.lemma = w[1]["Lemma"]
            word.pos = w[1]["PartOfSpeech"]
            word.ner = w[1]["NamedEntityTag"]
            if word.ner != "O":
                if word.ner in s.nes:
                    s.nes[word.ner].append(word.raw)
                else:
                    s.nes[word.ner] = [word.raw]
            s.words.append(word)
        return s

    def parse_document(self):
        # This function parses the entire input document through CoreNLP
        output = []

        for doc in self.batchcorenlp:
            output.append(doc)
        if len(output) > 1:
            print "Too many documents"
            exit(0)
        doc = output[0]
        sents = []

        # Parse sentences
        for s in doc["sentences"]:
            sent = Sentence()
            sent.parsetree = nltk.Tree(s["parsetree"])
            sent.depends = s["dependencies"]
            sent.raw = ' '.join(s["text"])

            # Parse words
            for w in s["words"]:
                word = Word()
                word.raw = w[0]
                word.lemma = w[1]["Lemma"]
                word.pos = w[1]["PartOfSpeech"]
                word.ner = w[1]["NamedEntityTag"]
                if word.ner != "O":
                    if word.ner in sent.nes:
                        sent.nes[word.ner].append(word.raw)
                    else:
                        sent.nes[word.ner] = [word.raw]
                sent.words.append(word)
            sents.append(sent)

        # Parse corefs
        for coref in doc["coref"][0]:
            location = int(coref[0][1])
            co_from = coref[0][0]
            co_to = coref[1][0]
            sents[location].corefs[co_from] = co_to

        return sents

    # BM25 Implementation
    def n(self, docs, word):
        return len([x for x in docs if word in x])

    def IDF(self, docs, word):
        N = len(docs)
        n = self.n(docs, word)
        return math.log((N - n + 0.5) / (n + 0.5))

    def f(self, doc, word):
        return doc.count(word)

    def score(self, doc, docs, keywords):
        k = 1.50
        b = 0.75
        score = 0
        avgl = sum([len(x) for x in docs]) / len(docs)
        for word in keywords:
            f = self.f(doc, word)
            idf = self.IDF(docs, word)
            num = f * (k + 1)
            dem = f + k * (1 - b + b * (len(doc) / avgl))
            score += idf * (num / dem)
        return score

    def rank_sentences(self, sents, keywords):
        """
        This function returns the sentences that best match the keywords
        and contain the part of speech desired. There is a chance that this
        function returns an empty list
        """
        scores = []
        raw_sents = [x.get_searchable() for x in sents]
        for i in xrange(len(raw_sents)):
            score = self.score(raw_sents[i], raw_sents, keywords)
            scores.append((sents[i], score))

        # Filter out no matches / no pos match
        #scores = [x for x in scores if x[1] > 0]
        scores = sorted(scores, key = lambda x: x[1], reverse = True)
        return [x[0] for x in scores]

    def yield_search(self, keywords):
        sents = self.rank_sentences(self.sents, keywords)
        for sent in sents:
            yield sent
        return
