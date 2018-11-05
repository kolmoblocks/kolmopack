#define WASM_EXPORT __attribute__((visibility("default")))
#define TOKEN_SIZE 2

void consoleLog(unsigned int num);
void consoleRightmostLog(unsigned int num);
void consoleLevelLog(unsigned int num);

char encoded_data[100000];
int encoded_data_size;

WASM_EXPORT
int* get_encoded_data_offset() {
  return &encoded_data[0];
}

WASM_EXPORT
void set_encoded_data_size(int size) {
  encoded_data_size = size;
}

WASM_EXPORT
char check_encoded_data_bit(int pos) {
  unsigned int bit_number = pos / 8;
  char bit_pos = pos % 8;
  char mask = 1<<(7-bit_pos);
  if (encoded_data[bit_number] & mask) {
    return 1;
  } else {
    return 0;
  }
}


char decoded_data[100000];
int decoded_data_size;
WASM_EXPORT
int* get_decoded_data_offset() {
  return &decoded_data[0];
}

WASM_EXPORT
int get_decoded_data_size(int size) {
  return decoded_data_size;
}



char huffman_tree_serialized[100000];
WASM_EXPORT
int* getHuffmanOffset() {
  return &huffman_tree_serialized[0];
}


typedef struct huffman_node_t
{
    char value[TOKEN_SIZE];          /* character(s) represented by this entry */
    struct huffman_node_t *left, *right;
} huffman_node_t;


// malloc huffman tree
huffman_node_t h_malloc[200000];
int h_malloc_pos=0;

int rightmost;

WASM_EXPORT
int* get_righmost_offset() {
  return &rightmost;
}

huffman_node_t *allocateNode(int level) {
  huffman_node_t *hn;

  hn = &h_malloc[h_malloc_pos];
  h_malloc_pos++;
  
  if (huffman_tree_serialized[rightmost] != '\0') {
    for (int j=0; j< TOKEN_SIZE; j++) {
        hn->value[j] = huffman_tree_serialized[rightmost];
        rightmost++;
    }
        // consoleLog(hn->value);
    return hn;
  }
  rightmost+= TOKEN_SIZE;
  // consoleLog(hn->value);
  hn->left = allocateNode(level+1);
  hn->right = allocateNode(level+1);
  return hn;
}

void printTree(huffman_node_t *node, int level) {
     consoleLevelLog(level);
     consoleLog(node->value);
     if (node->left) {
       printTree(node->left, level+1);
     }
     if (node->right) {
       printTree(node->right, level+1);
     }  
}


WASM_EXPORT
void buildHuffman()
{
   huffman_node_t *tree;
   rightmost = 0;  
   tree = allocateNode(0);
   printTree(tree, 0);
}

WASM_EXPORT
void decodeHuffman()
{
   huffman_node_t *tree, *c;  
   tree = allocateNode(0);
   int out_cur = 0; // cursor for output array 
   c = tree; // cursor for position within huffman tree


   for (unsigned int i = 0; i < encoded_data_size*8; i++) {
      // read the next bit within the encoded data
      if (check_encoded_data_bit(i)) {
       c = c->right;
      } else {
        c = c->left;
      }

      if (c->left) {
       continue;
      }

      // its a huffman tree leaf:
      // 1. write the symbol
      // 2. reset the huffman tree cursor
      for (int j=0; j< TOKEN_SIZE; j++) {
          decoded_data[out_cur] = c->value[j];
          out_cur++;
          decoded_data_size = out_cur;
      }
      c = tree;
   }
}




