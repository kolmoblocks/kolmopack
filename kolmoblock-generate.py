#!/usr/bin/env python3

import argparse
import queue
import heapq
import struct
import kolmo

FREQUENCY_THRESHOLD = 1
TMP_FILE = 'out/cur'

def get_counts(symbol_size, target):
    counts = {}
    while True:
        cur = target.read(symbol_size)
        if len(cur)<symbol_size:
            break
        counts[cur] = counts.get(cur, 0) + 1
    return counts

def print_counts():
    sorted_cs = sorted(cs.items(), key=lambda x:-x[1])
    for symbol, count in sorted_cs:
        if count < FREQUENCY_THRESHOLD:
            break
        print("{} [{}]: {:,}".format(repr(symbol), symbol.encode('hex'), count))




def build_huffman(counts, token_size):
    p = []
    all_else = 0
    for sym, count in cs.items():
        if count < FREQUENCY_THRESHOLD:
            all_else += count
            continue
        heapq.heappush(p,(count, sym))
    heapq.heappush(p,(all_else, b"\a" * token_size ))
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
    with open(TMP_FILE, 'w') as et_file: 
        for symbol,representation in sorted_table:
            et_file.write("{}|{}\n".format(representation, repr(symbol)))
    return kolmo.name_by_content(TMP_FILE, {
        "MIME": "text/plain",
        "tag": "huffman_encoding_table",  
        }
    )
        


def save_huffman_tree(tree, token_size):
    with open(TMP_FILE, 'wb') as ht_file:
        stack = [tree]
        while len(stack) > 0:
            (_, node) = stack.pop()
            if isinstance(node, bytes):
                ht_file.write(node)
                continue
            ht_file.write(str.encode("\0"*token_size))
            stack.append(node[1])
            stack.append(node[0])
    return kolmo.name_by_content(TMP_FILE, {
        "MIME": "application/octet-stream",
        "tag": "huffman_encoding_table binary serialized",
        "token_size": token_size,  
        }
    )

def load_huffman_tree(serialized_file, token_size):
    with open(serialized_file, 'rb') as s_file:
        def allocateNode():
            next_cell = s_file.read(token_size)
            if next_cell != b'\0'*token_size:
                return (10, next_cell)
            left = allocateNode()
            right = allocateNode()
            return (10, (left, right))
        root = allocateNode()
        return root



def save_compressed_data(symbol_size, codes, target_file):
    current = ""
    with open(TMP_FILE, 'w') as txt_cd_file: 
        while True:
            cur = target_file.read(symbol_size)
            if len(cur)< symbol_size:
                break
            if cur in codes:
                representation = codes[cur]
            else:
                literal = ""
                for each in cur:
                    literal += bin(each)[2:]
                representation = codes[b'\a'* symbol_size] + literal 
            txt_cd_file.write(representation)
            current += representation
    compressed_data_humans = kolmo.name_by_content(TMP_FILE, {
        "MIME": "text/plain",
        "tag": "huffman_encoded data human-readable",
        "token_size": symbol_size,  
        }
    )
    num_of_bytes = len(current) // (8)
    with open(TMP_FILE, 'wb') as cd_file: 
        for i in range(num_of_bytes):
            bytes = current[8*i:8*(i+1)]
            int_value = int(bytes, base=2)
            cd_file.write(int_value.to_bytes(1,'little'))
    compressed_data_binary = kolmo.name_by_content(TMP_FILE, {
        "MIME": "application/octet-stream",
        "tag": "huffman_encoded data binary",
        "token_size": symbol_size,  
        }
    )
    return compressed_data_humans, compressed_data_binary


parser = argparse.ArgumentParser()
parser.add_argument('--token_size', dest='token_size',default=1, type=int)
parser.add_argument('--target', dest='target', type=str)
parser.add_argument('--huffmantree', dest='huffmantree', default="", type=str)
args = parser.parse_args()


with open(args.target,'rb') as input_file: 
    cs = get_counts(args.token_size, input_file)

if args.huffmantree == "":
    huffman_tree = build_huffman(cs, args.token_size)
    htree_serialized_hash = save_huffman_tree(huffman_tree, args.token_size)
else:
    huffman_tree = load_huffman_tree(args.huffmantree, args.token_size)
    htree_serialized_hash = args.huffmantree    

encoding_table = generate_encoding(huffman_tree)
huffman_tree_humans = save_encoding_table(encoding_table)

with open(args.target,'rb') as input_file: 
    encoded_data_hash_humans, encoded_data_hash = save_compressed_data(args.token_size, encoding_table, input_file)

kolmo.generate_huffman_manifest(args.target, args.token_size, htree_serialized_hash, encoded_data_hash)
print("human readable encoded data: %s" % encoded_data_hash_humans)
print("human readable huffman tree %s" % huffman_tree_humans)


