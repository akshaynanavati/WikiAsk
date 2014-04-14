import nltk

class Classifier:

    def __init__(self, f):
        self.f = f

    def get_wh(self, t):
        if hasattr(t, "node") and t.node:
            if (t.node == "WDT" or t.node == "WP" or t.node == "WP$" or
                t.node == "WRB"):
                return t[0]
            else:
                for child in t:
                    wh = self.get_wh(child)
                    if wh:
                        return wh
        return None

    def classify_other(self, quest):
        if (quest.has_lemma("do") or quest.has_lemma("be") or
            quest.words[0].pos == "MD"):
            return "yesno"
        return None 

    def classify_wh(self, wh_word, quest):
        wh_word = wh_word.lower()
        if wh_word == "who" or wh_word == "whose":
            return "who"
        if (wh_word == "when" or wh_word == "where" or wh_word == "why" or
            wh_word == "what"):
            return wh_word
     
        after_index = [x.raw.lower() for x in quest.words].index(wh_word)+ 1
        after = quest.words[after_index].lemma
        if wh_word == "how":
            if after == "do":
                return "howdo"
            if after == "far":
                return "howfar"
            if after == "long":
                return "howlong"
            if after == "many":
                return "howmany"
            if after == "much":
                return "howmuch"
            return "howdo"

        return None

    def classify(self, quest):
        quest = self.f.parse_sentence(quest)
        if not quest:
            return None
        wh_word = self.get_wh(quest.parsetree)
        if wh_word:
            wh_type = self.classify_wh(wh_word, quest)
        else:
            wh_type = self.classify_other(quest)
        return wh_type


if __name__ == "__main__":
    print "Testing Classifying"
    c = Classifier()
    assert(c.classify("Who am I?") == "who")
    assert(c.classify("Where is he?") == "where")
    assert(c.classify("Where is the man who said hi?") == "where")
    print "Testing passed"
