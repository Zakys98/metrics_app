#include <stdio.h>

int main(){

    FILE *file = fopen("sizes", "w");
    fprintf(file, "char:%lu\n", sizeof(char));
    fprintf(file, "int:%lu\n", sizeof(int));
    fprintf(file, "long:%lu\n", sizeof(long));
    fprintf(file, "unsigned:%lu\n", sizeof(unsigned));
    fprintf(file, "unsigned long:%lu\n", sizeof(unsigned long));
    fprintf(file, "void *:%lu\n", sizeof(void*));
    fclose(file);

    return 0;
}