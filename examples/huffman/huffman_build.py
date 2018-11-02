import sys
import queue
import heapq
import struct

FREQUENCY_THRESHOLD = 1
SYMBOL_SIZE = 1 

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
        if count < FREQUENCY_THRESHOLD:
            break
        print("{} [{}]: {:,}".format(repr(symbol), symbol.encode('hex'), count))


class Node():
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right


def build_huffman(counts):
    p = []
    all_else = 0
    for sym, count in cs.items():
        if count < FREQUENCY_THRESHOLD:
            all_else += count
            continue
        heapq.heappush(p,(count, sym))
    heapq.heappush(p,(all_else, b"\a"))
    while len(p) > 1:
        l = heapq.heappop(p)
        r = heapq.heappop(p)
        heapq.heappush(p, (l[0]+r[0]- 0.0017,(l,r)))
    return heapq.heappop(p)


def generate_encoding(tree):
    codes = {}
    stack = [(tree, "")]
    while len(stack) > 0:
        (_, node), code = stack.pop()
        if isinstance(node, bytes):
            codes[node] = code
            continue
        left, right = node
        stack.append((left, code + "0"))
        stack.append((right, code + "1"))
    return codes

def save_encoding_table(codes):
    sorted_table = sorted(codes.items(), key=lambda x:len(x[1]))
    with open('data/encoding_table_{}.txt'.format(SYMBOL_SIZE), 'w') as et_file: 
        for symbol,representation in sorted_table:
            et_file.write("{}|{}\n".format(representation, repr(symbol)))


def save_huffman_tree(tree):
    with open('data/huffman_tree_{}.bin'.format(SYMBOL_SIZE), 'wb') as ht_file:
        stack = [tree]
        while len(stack) > 0:
            (_, node) = stack.pop()
            if isinstance(node, bytes):
                ht_file.write(node)
                continue
            ht_file.write(str.encode("\0"*SYMBOL_SIZE))
            stack.append(node[1])
            stack.append(node[0])


        


def save_compressed_data(symbol_size, codes,target):
    current = ""
    with open('data/compressed_data_{}.txt'.format(SYMBOL_SIZE), 'w') as txt_cd_file: 
        while True:
            cur = target.read(symbol_size)
            if len(cur)==0:
                break
            if cur in codes:
                representation = codes[cur]
            else:
                literal = ''.join(format(ord(x), 'b') for x in cur)
                representation = codes[b'\a'] + literal 
            txt_cd_file.write(representation)
            current += representation
    num_of_bytes = len(current) // (8)
    with open('data/compressed_data_{}.bin'.format(SYMBOL_SIZE), 'wb') as cd_file: 
        for i in range(num_of_bytes):
            bytes = current[8*i:8*(i+1)]
            # import pdb; pdb.set_trace()
            int_value = int(bytes, base=2)
            cd_file.write(int_value.to_bytes(1,'little'))
        tail = current[8*num_of_bytes:]

with open(sys.argv[1],'rb') as input_file: 
    cs = get_counts(SYMBOL_SIZE, input_file)

huffman_tree = build_huffman(cs)
save_huffman_tree(huffman_tree)
encoding_table = generate_encoding(huffman_tree)
save_encoding_table(encoding_table)
with open(sys.argv[1],'rb') as input_file: 
    save_compressed_data(SYMBOL_SIZE, encoding_table, input_file)


