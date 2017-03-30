#include <stdio.h>
#include "config.c"

#define NO_OF_SBOXES 16

// 8x8 SBoxes
extern char sbox_8_8[NO_OF_SBOXES][256];

// 6x4 SBoxes
extern char sboxes_6_4[NO_OF_SBOXES][64];

// SPN Permutation
extern char spn_permutation[16][8]; 

typedef struct {
	char block[NO_OF_SBOXES];
} StageBits;

typedef char* KeyType;

/*
void FiestelRound(StageBits *s, KeyType *key){
	char leftHalf[6], rightHalf[6];
	char lch, rch, ltemp, rtemp, tempval;
	int i, j;

	// expansion of inputs
	for (i=0; i<6; ++i) {
		lch = 0;
		rch = 0;
		for (j=0; j<8; ++j) {
			lch = lch  << 1;
			rch = rch << 1;
			tempval = expansion[i][j]-1;
			ltemp = s.block[8+tempval/8] << (7 - tempval % 8);
			rtemp = s.block[12+tempval/8] << (7 - tempval % 8)
			lch = lch | (ltemp >> 7);
			rch = rch | (rtemp >> 7);
		}
		leftHalf[i] = lch;
		rightHalf[i] = rch;
	}

	//key mixing
	for (i=0; i<6; ++i) {
		leftHalf[i] ^= key[i];
		rightHalf[i] ^= key[i+6]
	}

	char out[8];
	//substitution
	unsigned long left, right, lpad, rpad;
	left = 0;
	right = 0;
	left = leftHalf[0];
	right = rightHalf[0];
	for (i=1; i<6; ++i) {
		left = (left << 8) | leftHalf[i];
		right = (right << 8) | rightHalf[i];
	}
	j=42
	for (i=0; i<4; ++i) {
		lpad = left << (58-j);
		lpad = lpad >> (58-j);
		rpad = right << (58-j);
		rpad = rpad >> (58-j);
		out[i] = (0x0f && (lpad >> j));
		out[4+i] = (0x0f && (rpad >> j));
		j = j-6;
		lpad = left << (58-j);
		lpad = lpad >> (58-j);
		rpad = right << (58-j);
		rpad = rpad >> (58-j);
		out[i] = (out[i] << 4) | (lpad >> j);
		out[4+i] = (out[4+i] << 4) | (rpad >> j);
		j = j-6;
	}

	lpad = 0;
	rpad = 0;
	//permutation
	for (i=0; i<2; ++i) {
		for (j=0; j<8; j++) {
			lch = out[(i<<2) + j/8] << j;
			lch = lch >> (7-j);
			rpad = lpad;
			rpad = rpad << (64 - fperm[i][j]);
			rpad = lch | (rpad >> (fperm[i][j] - 1));
			lpad = lpad | (rpad << (fperm[i][j] - 1));
		}
	}
	for (i=2; i<4; ++i) {
		for (j=0; j<8; j++) {
			lch = out[4+ (i<<2) + j/8] << j;
			lch = lch >> (7-j);
			rpad = lpad;
			rpad = rpad << (64 - fperm[i][j]);
			rpad = lch | (rpad >> (fperm[i][j] - 1));
			lpad = lpad | (rpad << (fperm[i][j] - 1));
		}
	}
	for (i=7; i>=0; --i) {
		out[i] = lpad;
		lpad = lpad >> 8;
	}

	//xor lefthalf with fiestel output
	for (i=0; i<8; ++i) {
		out[i] ^= s.block[i];
	}

	for (i=0; i<8; ++i) {
		s.block[i] = s.block[8+i];
		s.block[8+i] = out[i];
	}
}
*/

void SPNRound(StageBits *s, StageBits *key){
	int i,j;

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++)
		s->block[i] ^= key->block[i]; 		

	// Substitution Layer
	for(i=0; i<NO_OF_SBOXES; i++)
		s->block[i] = sbox_8_8[i][s->block[i]];

	// Permutation Layer

	// Step-1: Create dummy result 
	StageBits new_s = {
		{ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 }
	};

	// Step-2: Compute actual result
	for(i=0; i<NO_OF_SBOXES; i++){
		for(j=0; j<8; j++){
			int bit_no = spn_permutation[i][j]; 
			new_s.block[i] |= ( s->block[bit_no / 8] & (1 << (bit_no % 8)) ) << j;
		}
	}

	// Step-3: Assign result to s
	*s = new_s;
}

int main(int argc, char** argv){
	// Test Vector
	StageBits s = { {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} };
	StageBits k = { {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1} };

	SPNRound(&s, &k);
	int i;
	for(i=0; i<16; i++)
		printf("%x,", s.block[i]);

	return 0;
}