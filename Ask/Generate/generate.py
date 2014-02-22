import random

gens = []
MAX_TRY = 10

class AlgError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def register_generation(fs):
    global gens
    for f in fs:
        gens += [f]

def generate(wiki, n):
    questions = []
    tries = 0
    if gens == []:
        raise AlgError ("no registered algorithm for question generation")
    while len(questions) < n and tries < MAX_TRY:
        algi = random.randint(0, len(gens) - 1)
        q = gens[algi](wiki)
        if q in questions:
            tries += 1
        else:
            questions += [q]
            tries = 0
    return questions