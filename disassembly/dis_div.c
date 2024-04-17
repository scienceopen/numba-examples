#include <stdlib.h>

int main(void){
   volatile float a = (float)rand();
   float x = a / 2.;
   return EXIT_SUCCESS;
}
