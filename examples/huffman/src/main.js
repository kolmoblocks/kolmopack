canvas = document.getElementById("container"); 
canvas.textContent = "old style";

async function loadKolmoblock() {
    const response = await fetch('../out/main.wasm');
    const buffer = await response.arrayBuffer();
    const module = await WebAssembly.compile(buffer);
    const instance = await WebAssembly.instantiate(module);
    return instance.exports;
}

loadKolmoblock().then(mm => {
  canvas.textContent = "hi peacock";
  const memory = mm.memory;
  const offset = mm.getStrOffset();
  const strBuf = new Uint8Array(memory.buffer, offset, 20);
  mm.decodeHuffman();
  const str = new TextDecoder().decode(strBuf);
  canvas.textContent = str;
}).catch(console.error);
