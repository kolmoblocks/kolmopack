#define WASM_EXPORT __attribute__((visibility("default")))

char encoded_data[1000];
int encoded_data_size;

WASM_EXPORT
char* get_encoded_data_offset() {
  return &encoded_data[0];
}

WASM_EXPORT
void set_encoded_data_size(int size) {
  encoded_data_size = size;
}


char decoded_data[10000];
int decoded_data_size;
WASM_EXPORT
char* get_decoded_data_offset() {
  return &decoded_data[0];
}

WASM_EXPORT
int get_decoded_data_size(int size) {
  return decoded_data_size;
}

void consoleLog (char num);

typedef int bool;
#define true 1
#define false 0

char huffman_tree_serialized[20];
int rightmost=1;
WASM_EXPORT
char* getHuffmanOffset() {
  return &huffman_tree_serialized[0];
}


typedef struct huffman_node_t
{
    char value;          /* character(s) represented by this entry */
    struct huffman_node_t *left, *right;
} huffman_node_t;


// malloc huffman tree
huffman_node_t h_malloc[20];
int h_malloc_pos;

huffman_node_t *allocateNode(int pos) {
  huffman_node_t *hn;

  hn = &h_malloc[h_malloc_pos];
  h_malloc_pos++;

  if (huffman_tree_serialized[pos] != '0') {
        hn->value = huffman_tree_serialized[pos];
        return hn;
  }
  int left_pos = rightmost;
  int right_pos = rightmost + 1;
  rightmost += 2;

  hn->left = allocateNode(left_pos);
  hn->right = allocateNode(right_pos);
  return hn;
}




WASM_EXPORT
void decodeHuffman()
{
   huffman_node_t *tree;  
   tree = allocateNode(0);
   int out_cur = 0; // cursor for output array 
   huffman_node_t *c = tree; // cursor for position within huffman tree
   for (int i = 0; i < 6; i++) {
     bool n = encoded[i]; // read the next bit within the encoded data
     if (n) {
       c = c->left;
     } else {
       c = c->right;
     }

     if (c->left) { // its not a huffman tree leaf yet
       continue;
     }

     // its a huffman tree leaf:
     // 1. write the symbol
     // 2. reset the huffman tree cursor
     decoded_data[out_cur] = c->value;
     out_cur++;
     decoded_data_size = out_cur;
     c = tree;
   }
}




