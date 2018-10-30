def load_encoding_table(source):
    sorted_table = sorted(codes.items(), key=lambda x:len(x[1]))
    with open('data/encoding_table.txt', 'r') as et_file: 
        for symbol :
            et_file.write("{}|{}\n".format(representation, symbol.encode("utf-8")))