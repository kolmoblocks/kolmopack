canvas = document.getElementById("container"); 
canvas.textContent = "old style";

async function loadKolmoblock() {
    const wasm_response = await fetch('../out/main.wasm');
    const buffer = await wasm_response.arrayBuffer();

    const huffmanTableResponse = await fetch('./huffman_tree');
    const huffmanTableRaw = await huffmanTableResponse.arrayBuffer();
    const huffmanTable = new Uint8Array(huffmanTableRaw, 0, huffmanTableRaw.byteLength);

    const datablockResponse = await fetch('./datablock');
    const datablockRaw = await datablockResponse.arrayBuffer();
    const datablock = new Uint8Array(datablockRaw, 0, datablockRaw.byteLength);

    const module = await WebAssembly.compile(buffer);
    const instance = await WebAssembly.instantiate(module, {env:{
        consoleLog: num => console.log(num)
    }});
    mm = instance.exports;

    const huffmanOffset = mm.getHuffmanOffset();
    const strBuf = new Uint8Array(mm.memory.buffer, huffmanOffset, huffmanTable.length);
    for (let i=0; i < huffmanTable.length; i++) {
      strBuf[i] = huffmanTable[i];
    }

    const encodedDataOffset = mm.get_encoded_data_offset();
    mm.set_encoded_data_offset(datablock.length);
    const encodedDataBuf = new Uint8Array(mm.memory.buffer, encodedDataOffset, datablock.length);
    for (let i=0; i < datablock.length; i++) {
      encodedDataBuf[i] = datablock[i];
    }

    return mm;
}

loadKolmoblock().then(mm => {
  canvas.textContent = "kolmoblock loaded, evaluating...";
  mm.decodeHuffman();

  const memory = mm.memory;
  const offset = mm.get_decoded_data_offset();
  const size = mm.get_decoded_data_size();

  const strBuf = new Uint8Array(memory.buffer, offset, size);
  const str = new TextDecoder().decode(strBuf);
  canvas.textContent = str;
}).catch(console.error);
