#ifndef HELPER_H
#define HELPER_H

#include "config.c"

#define NO_OF_SBOXES 16
#define NO_OF_ROUNDS 20

typedef struct {
	unsigned char block[NO_OF_SBOXES];
} StageBits;

void print_stage_op(StageBits *s){
	int i;
	for(i=0; i<NO_OF_SBOXES; i++)
		printf("0x%x, ", s->block[i]);
	printf("\n");
}

StageBits** trivial_key_expansion(StageBits *key){
	int i, j;

	StageBits **arr = malloc(sizeof(StageBits *)*NO_OF_ROUNDS);
	for(i=0; i<NO_OF_ROUNDS; i++){
		arr[i] = malloc(sizeof(StageBits));
		for(j=0; j<NO_OF_SBOXES; j++)
			arr[i]->block[j] = key->block[j] * (i+1);
	}

	return arr;
}

#endif