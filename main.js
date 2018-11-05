const KOLMOBLOCK = {
  "_target_id": "7cfd5747dd92443a30e230caf3f092a9b9880096f0d51d13433a9957c8d546d4",
  "_target_size": 18133,
  "_target_tag": "examples/chapter1.txt",
  "kolmoblocks": {
      "3d272a9f6": {
        "encoded_data": "bf751cdffed2a319c8ccfdad2da3fb990ff4762572fe952047610e2c33299567",
        "encoding_table_id": "90ec7319dff3815e827bc332ea5ec0b0c828e27fcec32771bd38f9a32c1f1b63",
        "symbol_size": 2,
        "wasm_id": "218d9e3e7cb68d30bfa4189270035597df87282abc2544e1ec4c216cfd6d08d8"
      }
    }
}

const MANIFEST = KOLMOBLOCK["kolmoblocks"]["3d272a9f6"]


canvas = document.getElementById("container"); 
canvas.textContent = "initalized, processing...";

async function loadKolmoblock(manifest) {
    const wasm_response = await fetch('/out/wasms/huffman2.wasm');
    const buffer = await wasm_response.arrayBuffer();

    const huffmanTableResponse = await fetch('/out/raw/' + manifest["encoding_table_id"]);
    const huffmanTableRaw = await huffmanTableResponse.arrayBuffer();
    const huffmanTable = new Uint8Array(huffmanTableRaw, 0, huffmanTableRaw.byteLength);
    console.log("serialized huffman-table size:", huffmanTableRaw.byteLength);

    const datablockResponse = await fetch('/out/raw/' + manifest["encoded_data"]);
    const datablockRaw = await datablockResponse.arrayBuffer();
    const datablock = new Uint8Array(datablockRaw, 0, datablockRaw.byteLength);
    console.log("serialized encoded data size:", datablockRaw.byteLength);

    const module = await WebAssembly.compile(buffer);
    const instance = await WebAssembly.instantiate(module, {env:{
        consoleLog: num => console.log("value is: ", num),
        consoleLevelLog: num => console.log("level is:", num),
        consoleRightmostLog: num => console.log("rightmost is:", num),
    }});

    mm = instance.exports;
    const huffmanOffset = mm.getHuffmanOffset();
    console.log("the offset for serialized huffman is:", huffmanOffset);

    console.log("the offset for rightmost is:", mm.get_righmost_offset());

    const strBuf = new Uint8Array(mm.memory.buffer, huffmanOffset, huffmanTable.length);
    for (let i=0; i < huffmanTable.length; i++) {
      strBuf[i] = huffmanTable[i];
    }
    const encodedDataOffset = mm.get_encoded_data_offset();
    console.log("the size of the encoded data is:", datablock.byteLength);
    console.log("the offset for encoded data is:", encodedDataOffset);
    console.log("while the total size of the wasm instance block is:", mm.memory.buffer.byteLength);
    mm.set_encoded_data_size(datablock.byteLength);
    const encodedDataBuf = new Uint8Array(mm.memory.buffer, encodedDataOffset, datablock.byteLength);
    for (let i=0; i < datablock.byteLength; i++) {
      encodedDataBuf[i] = datablock[i];
    }
    return mm;
}

loadKolmoblock(MANIFEST).then(mm => {
  canvas.textContent = "kolmoblock loaded, evaluating...";

  mm.decodeHuffman();

  const memory = mm.memory;
  const offset = mm.get_decoded_data_offset();
  const size = mm.get_decoded_data_size();


  const strBuf = new Uint8Array(memory.buffer, offset, size+1);
  const str = new TextDecoder().decode(strBuf);
  canvas.textContent = str;
}).catch(console.error);
