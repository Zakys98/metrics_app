#include <stdio.h>

int main(){

    printf("char:%d\n", sizeof(char));
    printf("int:%d\n", sizeof(int));
    printf("long:%d\n", sizeof(long));
    printf("unsigned:%d\n", sizeof(unsigned));
    printf("unsigned long:%d\n", sizeof(unsigned long));
    printf("*:%d\n", sizeof(void*));

    return 0;
}