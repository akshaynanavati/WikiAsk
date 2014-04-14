import nltk

def strings_within(str1, str2):
    string1 = str1.split()
    string2 = str2.split()
    ret = True
    for item in string1:
        if item not in string2:
            ret = False
    if ret:
        return True
    for item in string2:
        if item not in string1:
            return False
    return True

def rel_match(qgov, qdep, sgov, sdep):
    if qgov == sgov or strings_within(qgov, sgov):
        if qdep == sdep or strings_within(qdep, sdep):
            return True
    if qgov == sdep or strings_within(qgov, sdep):
        if qdep == sgov or strings_within(qdep, sgov):
            return True
    return False

def get_deps(sent):
    info = {}
    # Get subjects
    for depend in sent.depends:
        if depend[0] == "nsubj" or depend[0] == "nsubjpass":
            subj = depend[2]
            action = depend[1]
            if subj in sent.corefs:
                subj = sent.corefs[subj]
            elif sent.has_lemma(subj):
                subj = sent.get_lemma(subj)
            action = sent.get_lemma(action)
            info[subj] = {"acts" : {action : False}}
    # Get subject info
    for depend in sent.depends:
        if depend[0] == "conj_and" or depend[0] == "conj_but":
            action = sent.get_lemma(depend[2])
            for subj in info:
                if action in info[subj]["acts"]:
                    info[subj]["acts"][action] = False
        if depend[0] == "conj_negcc":
            action = sent.get_lemma(depend[2])
            for subj in info:
                if action in info[subj]["acts"]:
                    info[subj]["acts"][action] = True
        if depend[0] == "neg":
            action = sent.get_lemma(depend[1])
            for subj in info:
                if action in info[subj]["acts"]:
                    info[subj]["acts"][action] = True
        if depend[0] == "advmod" and depend[2] == "not":
            action = sent.get_lemma(depend[1])
            for subj in info:
                if action in info[subj]["acts"]:
                    info[subj]["acts"][action] = True
    return info

def get_yesno(sent, parsed_quest):
    # Get sentence info
    sinfo = get_deps(sent)
    qinfo = get_deps(parsed_quest)
    for qsubj in qinfo:
        for ssubj in sinfo:
            if qsubj == ssubj or strings_within(qsubj, ssubj):
                for qact in qinfo[qsubj]["acts"]:
                    if qact not in sinfo[ssubj]["acts"]:
                        return "No"
                    if (qinfo[qsubj]["acts"][qact] != 
                        sinfo[ssubj]["acts"][qact]):
                        return "No"
    return "Yes"

def exact_match(parsed_quest, f):
    # Get string
    to_match = []
    subj = []
    verb = None
    for i in xrange(1, len(parsed_quest.words)):
        word = parsed_quest.words[i]
        if word.pos not in ["NN", "NNP", "NNS", "NNPS"]:
            to_match = parsed_quest.words[i:-1]
            subj = parsed_quest.words[1:i]
            break
    to_match = ' '.join([x.raw for x in to_match])
    subj = ' '.join([x.raw for x in subj])
    for sent in f.sents:
        raw = ' '.join([x.raw for x in sent.words])
        if to_match in raw:
            for coref in sent.corefs:
                if strings_within(subj, coref):
                    return "Yes"
            if subj in raw or strings_within(subj, raw):
                return "Yes"
    return None 

def answer(quest, f):
    tokens = nltk.word_tokenize(quest)
    parsed_quest = f.parse_sentence(quest)
    if not parsed_quest:
        return None
    res = exact_match(parsed_quest, f)
    if res:
        return res
    for sent in f.yield_search(tokens):
        answer = get_yesno(sent, parsed_quest)
        if answer:
            return answer
    return None
