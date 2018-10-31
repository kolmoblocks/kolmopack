#define WASM_EXPORT __attribute__((visibility("default")))

void consoleLog (char num);

typedef int bool;
#define true 1
#define false 0

typedef struct huffman_node_t
{
    char value;          /* character(s) represented by this entry */
    struct huffman_node_t *left, *right;
} huffman_node_t;


char huffman_tree_serialized[20];
int rightmost=1;
WASM_EXPORT
char* getHuffmanOffset() {
  return &huffman_tree_serialized[0];
}

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


bool encoded[] = {true, false, true, false, false, true};

char outStr[20];
WASM_EXPORT
char* getStrOffset () {
  return &outStr[0];
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
     outStr[out_cur] = c->value;
     out_cur++;
     c = tree;
   }
}




