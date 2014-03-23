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

    def classify(self, sent):
        sent_tree = self.parser.parse(sent)

        if sent_tree.node != "SBARQ":
            print "Warning, root is not a SBARQ (direct question)"

        (wh_kind, wh_word) = self.get_wh(sent_tree)

        return (wh_kind, wh_word)
