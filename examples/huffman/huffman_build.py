import sys

def get_counts(symbol_size, target):
    counts = {}
    while True:
        cur = target.read(symbol_size)
        if len(cur)==0:
            break
        counts[cur] = counts.get(cur, 0) + 1
    return counts

cs = get_counts(2, open(sys.argv[1],'r'))

sorted_cs = sorted(cs.items(), key=lambda x:-x[1])
for symbol, count in sorted_cs:
    print "{} [{}]: {:,}".format(repr(symbol), symbol.encode('hex'), count)
