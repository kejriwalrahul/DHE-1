#include <stdio.h>
#include "sbox.c"

const int NO_OF_SBOXES = 16;

// 8x8 SBoxes
extern char sbox_8_8[NO_OF_SBOXES][256];
extern char inv_sbox_8_8[NO_OF_SBOXES][256];

// 6x4 SBoxes
extern char sboxes_6_4[NO_OF_SBOXES][64];

typedef struct {
	char block[NO_OF_SBOXES];
} StageBits;

void FiestelRound(StageBits *s){
	
}

void SPNRound(StageBits *s, StageBits *key){
	int i;

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] ^= key.block[i]; 		

	// Substitution
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] = sbox_8_8[i][s.block[i]];

	// Permutation
	StageBits new_s = 
}

int main(int argc, char** argv){
	// Test Vector
	StageBits s = { {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} };

	return 0;
}