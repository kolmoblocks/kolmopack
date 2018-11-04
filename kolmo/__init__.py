import hashlib, shutil
import json
import os.path

def get_name_and_size(target):
    size = 0
    m = hashlib.sha256()
    with open(target, 'rb') as target_file:
        while True:
            cur = target_file.read(1)
            if len(cur)==0:
                break
            size += 1
            m.update(cur)
    hex_identity = m.hexdigest()
    return hex_identity, size

def name_by_content(target, attributes):
    hex_identity, size = get_name_and_size(target)
    shutil.copyfile(target, 'out/raw/'+ hex_identity)        
    with open('out/header/'+hex_identity+'.json', 'w') as header_file:
        attributes.update({ 
            "id": hex_identity,
            "size": size,
        })
        header_file.write(json.dumps(attributes, sort_keys=True, indent=4))
    return hex_identity


# huffman_wasms maps the huffman encoding options to
# the id of the wasm to decode it
huffman_wasms = {
   1: "7ec006317196777f657837df911e0ea1efe405d3655aaaa2023ae26ae8aafd26",
}

def _generate_manifest_key(attributes):
    return attributes["wasm_id"][:4]+ str(attributes["symbol_size"]) + attributes["encoding_table_id"][:4]

def generate_huffman_manifest(target, symbol_size, huffman_tree, encoded_data):
    hex_identity, size = get_name_and_size(target)
    hex_path = 'out/public/'+hex_identity +'.json'
    attributes = { 
        "wasm_id": huffman_wasms[symbol_size],
        "encoding_table_id": huffman_tree,
        "encoded_data": encoded_data,
        "symbol_size": symbol_size,
    }

    cur = {
        "_target_id": hex_identity,
        "_target_tag": target,
        "_target_size": size,
        "kolmoblocks": {
        }
    }
    if os.path.isfile(hex_path):
        with open(hex_path, 'r') as prexisted_file:
            cc = prexisted_file.read()
            cur = json.loads(cc)
    
    cur["kolmoblocks"][_generate_manifest_key(attributes)] = attributes
    with open('out/public/'+hex_identity +'.json', 'w') as header_file:
        header_file.write(json.dumps(cur, sort_keys=True, indent=4))
    return hex_path

