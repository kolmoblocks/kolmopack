import sys
import queue
import heapq



def get_counts(symbol_size, target):
    counts = {}
    while True:
        cur = target.read(symbol_size)
        if len(cur)==0:
            break
        counts[cur] = counts.get(cur, 0) + 1
    return counts

def print_counts():
    sorted_cs = sorted(cs.items(), key=lambda x:-x[1])
    for symbol, count in sorted_cs:
        if count < 100:
            break
        print("{} [{}]: {:,}".format(repr(symbol), symbol.encode('hex'), count))


class Node():
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right


def build_huffman(counts):
    p = []
    for sym, count in cs.items():
        if count < 10:
            continue
        heapq.heappush(p,(count, sym))
    while len(p) > 1:
        l = heapq.heappop(p)
        r = heapq.heappop(p)
        heapq.heappush(p, (l[0]+r[0]- 0.17,(l,r)))
    return heapq.heappop(p)


def generate_encoding(tree):
    codes = {}
    stack = [(tree, "")]
    while len(stack) > 0:
        (_, node), code = stack.pop()
        if isinstance(node, str):
            codes[node] = code
            continue
        left, right = node
        stack.append((left, code + "0"))
        stack.append((right, code + "1"))
    return codes

def save_encoding_table(codes):
    sorted_table = sorted(codes.items(), key=lambda x:len(x[1]))
    with open('encoding_table.txt', 'w') as et_file: 
        for symbol,representation in sorted_table:
            et_file.write("{}|{}\n".format(representation, symbol.encode("utf-8")))



cs = get_counts(3, open(sys.argv[1],'r'))
huffman_tree = build_huffman(cs)
encoding_table = generate_encoding(huffman_tree)
save_encoding_table(encoding_table)
print(encoding_table)


