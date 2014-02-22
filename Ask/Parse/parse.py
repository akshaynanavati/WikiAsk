#right now all it does is returun a line by line list of the file
#contents (where each line is a space seperated list of strings. 
# We probably will want a better parser later
def parse(fname):
    f = open(fname)
    ret = []
    for line in f:
        ret = ret + [line.split(" ")]
    f.close()
    return ret    