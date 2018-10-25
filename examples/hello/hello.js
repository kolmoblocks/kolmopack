WebAssembly.instantiateStreaming(fetch('hello.wasm'))
.then(obj => {
   console.log("hello!");
   console.log(obj.instance.exports.add(1, 2));  // "3"
});
