import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tag.stanford import NERTagger

from itertools import groupby
from collections import defaultdict
import math

import json
import jsonrpclib

import re

class Finder:

    class Paragraph:
        def __init__(self):
            self.text = ""
            self.sents = []

    class Sentence:
        def __init__(self):
            self.raw = ""
            self.words = []
            self.pos = []
            self.lemmas = []
            self.nes = {}
            self.corefs = {}

    def __init__(self, filename):
        with open(filename, 'r') as inputfile:
            self.raw = inputfile.read()
        paras = self.raw.split('\n\n')
        self.paras = [x for x in paras if len(x) > 0]

        print 1
        from corenlp import StanfordCoreNLP
        self.corenlp = StanfordCoreNLP("stanford-corenlp-full-2014-01-04")
        print 2
        
        print len(self.paras)
        #self.sents = self.parse_document(filename)
        #self.document = PlaintextCorpusReader("", filename)
        #self.paras = self.document.paras()
        #self.sents = self.parse_document()
        #self.flatparas = self.parse_paragraphs()
        #self.sents = self.document.sents()
        #self.words = self.document.words()
        #self.entities = self.get_entities(self.document.raw())

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

    def parse_paragraph(self, para):
        """
        This function takes in the document and parses it through the
        standford corenlp, and then pieces the document back together 
        creating an array of Word objects, which each contain useful
        information about the word
        """
        #server = jsonrpclib.Server("http://localhost:8080")
        #result = json.loads(server.parse(doc))
        #from corenlp import StanfordCoreNLP
        #corenlp_dir = "stanford-corenlp-full-2014-01-04"
        #parsed = server.batch_parse(filename)
        #corenlp_dir = "Stanford-corenlp-full-2014-01-04"
        #corenlp = StanfordCoreNLP(corenlp_dir)

        #parse = json.loads(server.parse(para))
        parse = self.corenlp.raw_parse(para)
    
        p = self.Paragraph()
        # Parse the sentence structure and information
        for sent in parse["sentences"]:
            s = self.Sentence()
            s.raw = sent["text"]
            for word in s.words:
                s.words.append(word[0])
                s.pos.append(word[1]["PartOfSpeech"])
                s.lemmas.append(word[1]["Lemma"])
                tag = word[1]["NamedEntityTag"]
                if tag != "O":
                    if tag in s.nes:
                        s.nes[tag].append(word[0])
                    else:
                        s.nes[tag] = [word[0]]
            p.sents.append(s)

            # If there are any corefs, mark them
        if "coref" in parse:
            r = re.compile("[\(\),\[\]\-\s]+")
            for coref in parse["coref"][0]:
                first = re.split('"', coref)
                word_from = first[1]
                word_to = first[3]

                numbers = re.split("[\(,]+", coref)
                loc = int(numbers[1]) - 1

                p.sents[loc].corefs[word_from] = word_to
        return p

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

    def rank_paragraphs(self, keywords):
        """
        This function returns the index of the best matching paragraphs, in
        order of best to worst
        """
        scores = []
        for i in xrange(len(self.paras)):
            para = self.paras[i]
            score = self.score(para, self.paras, keywords)
            scores.append((i, score))
        
        # Filter out no matches
        scores = [x for x in scores if x[1] > 0]
        scores = sorted(scores, key = lambda x: x[1], reverse = True)
        return [x[0] for x in scores]

    def rank_sentences(self, para, keywords):
        """
        This function returns the sentences that best match the keywords
        and contain the part of speech desired. There is a chance that this
        function returns an empty list
        """
        scores = []
        sents = [x.raw for x in para.sents]
        for sent in sents:
            score = self.score(sent, sents, keywords)
            scores.append((sent, score))

        # Filter out no matches / no pos match
        scores = [x for x in scores if x[1] > 0]
        #scores = [x for x in scores if self.sentence_has_pos(pos, x[0])]
        scores = sorted(scores, key = lambda x: x[1], reverse = True)
        return [x[0] for x in scores]

    def yield_search(self, keywords):
        para_indices = self.rank_paragraphs(keywords)
        for index in para_indices:
            para = self.paras[index]
            stanford_para = self.parse_paragraph(para)
            sents = self.rank_sentences(stanford_para, keywords)
            for sent in sents:
                yield sent
        return
