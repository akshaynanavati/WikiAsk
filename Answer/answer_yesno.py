import nltk

def get_do(sent, parsed_quest):
    for depend in sent.depends:
        if depend[0] == "nsubj":
            sent_trait = depend[1]
            sent_trait = sent.lemmas[sent.words.index(sent_trait)]
            sent_trait = (sent_trait, True)
            sent_subj = depend[2].lower()
        if depend[0] == "neg" and depend[1] == sent_trait:
            sent_trait = (sent_trait[0], False) 
    for depend in parsed_quest.depends:
        if depend[0] == "nsubj":
            trait = depend[1]
            trait = parsed_quest.lemmas[parsed_quest.words.index(trait)]
            trait = (trait, True)
            subj = depend[2].lower()
        if depend[0] == "neg" and depend[1] == trait:
            trait = (trait[0], False)
    if sent_trait == trait and sent_subj == subj:
        return "Yes"
    return "No"

def get_yesno(sent, parsed_quest):
    return None
    if parsed_quest.lemmas[0] == "do":
        return get_do(sent, parsed_quest)
    return None

def answer(quest, f):
    tokens = nltk.word_tokenize(quest)
    parsed_quest = f.parse_sentence(quest)
    for sent in f.yield_search(tokens):
        answer = get_yesno(sent, parsed_quest)
        if answer:
            print quest, answer
            return answer
    return None
