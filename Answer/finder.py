import nltk
from nltk.corpus import PlaintextCorpusReader

import math

class Finder:

    def __init__(self, filename):
        self.document = PlaintextCorpusReader("", filename)
        self.paras = self.document.paras()
        self.flatparas = self.parse_paragraphs()
        self.sents = self.document.sents()
        self.words = self.document.words()
        #self.entities = self.get_entities()

    def parse_paragraphs(self):
        """
        This function takes the default result of the paragraph parsing
        from PlaintextCorpusReader and flattens the list
        """
        paras = []
        for para in self.document.paras():
            paras.append([item for sublist in para for item in sublist])
        return paras

    # Entity Construction
    def extract_entity_names(self, t, kind):
        # list of kinds: ORGANIZATION, PERSON, LOCATION, DATE, TIME,
        # PERCENT, MONEY, FACILITY, GPE
        entities = []
        if hasattr(t, "node") and t.node:
            if t.node == kind:
                entity = ' '.join([child[0] for child in t])
                entities.append(entity)
            else:
                for child in t:
                    entities.extend(self.extract_entity_names(child, kind))
        return entities

    def get_entities(self, text, kind):
        #text = self.document.raw()
        sents = nltk.sent_tokenize(text)
        sents = [nltk.word_tokenize(sent) for sent in sents]
        sents = [nltk.pos_tag(sent) for sent in sents]
        chunked = nltk.batch_ne_chunk(sents)
        entities = []
        for tree in chunked:
            entities.extend(self.extract_entity_names(tree, kind))
        print set(entities)
        return set(entities)

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
        for i in xrange(len(self.flatparas)):
            para = self.flatparas[i]
            score = self.score(para, self.paras, keywords)
            scores.append((i, score))
        
        # Filter out no matches
        scores = [x for x in scores if x[1] > 0]
        scores = sorted(scores, key = lambda x: x[1], reverse = True)
        return [x[0] for x in scores]

    def sentence_has_pos(self, pos, sent):
        sent = ' '.join(sent)
        sent = nltk.word_tokenize(sent)
        tags = nltk.pos_tag(sent)
        tags = [x[1] for x in nltk.pos_tag(sent)]
        return pos in tags

    def rank_sentences(self, sents, keywords):
        """
        This function returns the sentences that best match the keywords
        and contain the part of speech desired. There is a chance that this
        function returns an empty list
        """
        scores = []
        for sent in sents:
            score = self.score(sent, sents, keywords)
            scores.append((sent, score))

        # Filter out no matches / no pos match
        scores = [x for x in scores if x[1] > 0]
        #scores = [x for x in scores if self.sentence_has_pos(pos, x[0])]
        scores = sorted(scores, key = lambda x: x[1], reverse = True)
        return [x[0] for x in scores]

    def search(self, pos, keywords):
        para_indices = self.rank_paragraphs(keywords)
        for index in para_indices:
            para = self.paras[index]
            sents = self.rank_sentences(para, keywords)
            if sents:
                return sents[0]
        return None

    # Different searches
    def search_who(self, keywords):
        para_indices = self.rank_paragraphs(keywords)
        for index in para_indices:
            para = self.paras[index]
            sents = self.rank_sentences(para, keywords)
            for sent in sents:
                sent = ' '.join(sent)
                entities = self.get_entities(sent, "PERSON")
                print sent
                print entities
                return
        return None

c = Finder("a1.txt")
print c.search_who(["plays", "Tottenham", "Hotspur", "United", "States", "national", "team"])
