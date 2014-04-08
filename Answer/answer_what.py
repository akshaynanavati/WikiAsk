import nltk

"""
def answer_what(sent, parsed_quest):
    tree = sent.parsetree
    if hasattr(tree, "node") and tree.node:
        if (tree.node in [])
"""
def answer(quest, f, kind):
    """
    This function is used to answer the what question, given the 
    question as a complete setence and the finder object
    """
    """
    tokens = nltk.word_tokenize(quest)
    for sent in f.yield_search(tokens):
        parsed_quest = f.parse_sentence(quest)
        if kind == "whatequiv":
            answer = answer_equiv(sent, parsed_quest)
        elif kind == "whattype":
            answer = answer_type(sent, parsed_quest)
        elif kind == "whatprep":
            answer = answer_prep(sent, parsed_quest)
        elif kind == "whatrole":
            answer = answer_role(sent, parsed_quest)
        elif kind == "whattime":
            answer = answer_time(sent, parsed_quest)
        elif kind == "whatmeas":
            answer = answer_meas(sent, parsed_quest)
        if answer:
            return answer
    """
    return None

