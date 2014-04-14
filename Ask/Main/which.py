import lib

def generate(npvp):
    pruned = npvp # lib.prune(npvp, "SBAR")
    cci = lib.find_index(pruned, "CC")
    prunei = cci
    leaves = pruned.leaves()[:prunei]
    return ["Which"] + leaves[1:]
    
