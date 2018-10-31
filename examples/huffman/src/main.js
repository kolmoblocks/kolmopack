canvas = document.getElementById("container"); 
canvas.textContent = "old style";

async function loadKolmoblock() {
    const wasm_response = await fetch('../out/main.wasm');
    const buffer = await wasm_response.arrayBuffer();

    const huffmanTableResponse = await fetch('./huffman_tree.html');
    const huffmanTableRaw = await huffmanTableResponse.arrayBuffer();
    const huffmanTable = new Uint8Array(huffmanTableRaw, 0, huffmanTableRaw.byteLength);

    const module = await WebAssembly.compile(buffer);
    const instance = await WebAssembly.instantiate(module, {env:{
        consoleLog: num => console.log(num)
    }});
    mm = instance.exports;

    const huffmanOffset = mm.getHuffmanOffset();
    console.log("the offset is: ", huffmanOffset);
    const strBuf = new Uint8Array(mm.memory.buffer, huffmanOffset, huffmanTable.length);
    for (let i=0; i < huffmanTable.length; i++) {
      strBuf[i] = huffmanTable[i];
    }
    return mm;
}

loadKolmoblock().then(mm => {
  canvas.textContent = "hi peacock";
  mm.decodeHuffman();

  const memory = mm.memory;
  const offset = mm.getStrOffset();
  const strBuf = new Uint8Array(memory.buffer, offset, 20);
  const str = new TextDecoder().decode(strBuf);
  canvas.textContent = str;
}).catch(console.error);
