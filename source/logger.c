#include <stdio.h>
#include <string.h>

#include "../include/logger.h"

struct {
    FILE *output;
    char filename[30];
} logger;

int loggerInit(const char *filename){
    strcpy(logger.filename, filename);
    logger.output = fopen(logger.filename, "w");
    if(logger.output == NULL){
        fprintf(stderr, "Couldn not initialize logger\n");
        return 1;
    }
    return 0;
}

void loggerLog(){

}

void loggerDestroy(){
    fclose(logger.output);
}