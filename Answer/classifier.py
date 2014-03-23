from stat_parser import Parser
import nltk

class Classifier:

    def __init__(self):
        self.parser = Parser()

    def get_wh(self, t):
        if hasattr(t, "node") and t.node:
            if (t.node == "WDT" or t.node == "WP" or t.node == "WP$" or
                t.node == "WRB"):
                return (t.node, t[0])
            else:
                for child in t:
                    wh = self.get_wh(child)
                    if wh:
                        return wh
        return None

    def classify_wh(self, wh_word, tokens):
        if (wh_word == "when" or wh_word == "where" or wh_word == "why" or
            wh_word == "who"):
            return wh_word
       
        tokens = [x.lower() for x in tokens]
        after = tokens[tokens.index(wh_word) + 1]
        if wh_word == "how":
            if after == "do" or after == "did":
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

        return wh_word

    def classify(self, quest)
        quest_tree = self.parser.parse(quest)
        tokens = nltk.word_tokenize(quest)

        if sent_tree.node != "SBARQ":
            print "Warning, root is not a SBARQ (direct question)"

        (wh_kind, wh_word) = self.get_wh(quest_tree)
        wh_type = self.classify_wh(wh_word, tokens)

        return wh_type


if __name__ == "__main__":
    print "Testing Classifying"
    c = Classifier()
    assert(c.classify("Who am I?") == "who")
    assert(c.classify("Where is he?") == "where")
    assert(c.classify("Where is the man who said hi?") == "where")
    print "Testing passed"
