#include <stdio.h>
#include "config.c"

const int NO_OF_SBOXES = 16;

// 8x8 SBoxes
extern char inv_sbox_8_8[NO_OF_SBOXES][256];

// 6x4 SBoxes
extern char sboxes_6_4[NO_OF_SBOXES][64];

// Inverse SPN Permutation
extern char inv_spn_permutation[16][8]; 

typedef struct {
	char block[NO_OF_SBOXES];
} StageBits;

void SPNRound(StageBits *s, StageBits *key){
	int i,j;

	// Inverse Permutation Layer

	// Step-1: Create dummy result 
	StageBits new_s = {
		{ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 }
	};

	// Step-2: Compute actual result
	for(i=0; i<NO_OF_SBOXES; i++){
		for(j=0; j<8; j++){
			int bit_no = inv_spn_permutation[i][j]; 
			new_s.block[i] |= s.block[bit_no / 8][bit_no % 8] << j;
		}
	}

	// Step-3: Assign result to s
	*s = new_s;

	// Inverse Substitution Layer
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] = inv_sbox_8_8[i][s.block[i]];

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++)
		s.block[i] ^= key.block[i]; 		
}