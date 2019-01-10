#include "emscripten.h"
#include <stdlib.h>

char msg[] = "Hello";

EMSCRIPTEN_KEEPALIVE
int main() {
    return 0;
}

EMSCRIPTEN_KEEPALIVE
unsigned char get_result_offset() {
    return *msg;
}

EMSCRIPTEN_KEEPALIVE
int get_result_size() {
    return 5;
}
