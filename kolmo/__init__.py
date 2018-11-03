import hashlib, shutil
import json

def name_by_content(target, attributes):
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
    shutil.copyfile(target, 'out/raw/'+ hex_identity)        
    with open('out/header/'+hex_identity+'.json', 'w') as header_file:
        attributes.update({ 
            "id": hex_identity,
            "size": size,
        })
        header_file.write(json.dumps(attributes, sort_keys=True, indent=4))