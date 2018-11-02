canvas = document.getElementById("container"); 
canvas.textContent = "old style";

async function loadKolmoblock() {
    const wasm_response = await fetch('../out/main.wasm');
    const buffer = await wasm_response.arrayBuffer();

    const huffmanTableResponse = await fetch('../data/huffman_tree_1.bin');
    const huffmanTableRaw = await huffmanTableResponse.arrayBuffer();
    const huffmanTable = new Uint8Array(huffmanTableRaw, 0, huffmanTableRaw.byteLength);

    const datablockResponse = await fetch('../data/compressed_data_1.bin');
    const datablockRaw = await datablockResponse.arrayBuffer();
    const datablock = new Uint8Array(datablockRaw, 0, datablockRaw.byteLength);

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

loadKolmoblock().then(mm => {
  canvas.textContent = "kolmoblock loaded, evaluating...";
  // for (let i=0; i<10; i++) {
  //   console.log("the ", i, "th bit is ", mm.check_encoded_data_bit(i));
  // }
  mm.decodeHuffman();

  const memory = mm.memory;
  const offset = mm.get_decoded_data_offset();
  const size = mm.get_decoded_data_size();

  const strBuf = new Uint8Array(memory.buffer, offset, size+1);
  const str = new TextDecoder().decode(strBuf);
  canvas.textContent = str;
}).catch(console.error);
