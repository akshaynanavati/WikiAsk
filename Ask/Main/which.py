import lib

def generate(npvp):
    pruned = lib.prune(npvp, "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["which"] + leaves[1:]
    
