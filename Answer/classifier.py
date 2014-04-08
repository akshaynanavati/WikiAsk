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
        if (quest.lemmas[0] == "do" or quest.lemmas[0] == "be" or
            quest.pos[0] == "MD"):
            return "yesno"
        return None 

    def classify_wh(self, wh_word, quest):
        wh_word = wh_word.lower()
        if (wh_word == "when" or wh_word == "where" or wh_word == "why" or
            wh_word == "who"):
            return wh_word
     
        after_index = [x.lower() for x in quest.words].index(wh_word) + 1
        after = quest.lemmas[after_index]
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

        if wh_word == "what":
            if False:
                return "whatequiv"
            if after == "type" or after == "kind":
                return "whattype"
            if False:
                return "whatprep"
            if False:
                return "whatrole"
            if False:
                return "whattime"
            if False:
                return "whatmeas"

        return None

    def classify(self, quest):
        quest = self.f.parse_sentence(quest)
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
