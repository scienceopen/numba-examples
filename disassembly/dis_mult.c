#include <stdlib.h>

int main(void){
   volatile float a = (float)rand();
   float x = a * 0.5;
   return EXIT_SUCCESS;
}
