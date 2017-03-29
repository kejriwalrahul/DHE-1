#include <stdio.h>
#include "config.c"

const int NO_OF_SBOXES = 16;

// 8x8 SBoxes
extern char sbox_8_8[NO_OF_SBOXES][256];
extern char inv_sbox_8_8[NO_OF_SBOXES][256];

// 6x4 SBoxes
extern char sboxes_6_4[NO_OF_SBOXES][64];

typedef struct {
	char block[NO_OF_SBOXES];
} StageBits;

void FiestelRound(StageBits *s, KeyType *key){
	char rightHalf[8];
	char ch;
	int i;
	for (i=0; i<64; ++i) {
		rightHalf[i] = 
	}
}

void SPNRound(StageBits *s, StageBits *key){
	int i,j;

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] ^= key.block[i]; 		

	// Substitution Layer
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] = sbox_8_8[i][s.block[i]];

	// Permutation Layer

	// Step-1: Create dummy result 
	StageBits new_s = {
		{ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 }
	};

	// Step-2: Compute actual result
	for(i=0; i<NO_OF_SBOXES; i++){
		for(j=0; j<8; j++){
			int bit_no = spn_permutation[i][j]; 
			new_s.block[i] |= s.block[bit_no / 8][bit_no % 8] << j;
		}
	}

	// Step-3: Assign result to s
	*s = new_s;
}

int main(int argc, char** argv){
	// Test Vector
	StageBits s = { {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} };

	return 0;
}