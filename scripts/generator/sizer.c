#include <stdio.h>

int main(){

    printf("char:%lu\n", sizeof(char));
    printf("int:%lu\n", sizeof(int));
    printf("long:%lu\n", sizeof(long));
    printf("unsigned:%lu\n", sizeof(unsigned));
    printf("unsigned long:%lu\n", sizeof(unsigned long));
    printf("*:%lu\n", sizeof(void*));

    return 0;
}