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
	char leftHalf[6], rightHalf[6];
	char lch, rch, ltemp, rtemp;
	int i, j;

	// expansion of inputs
	for (i=0; i<6; ++i) {
		lch = 0;
		rch = 0;
		for (j=0; j<8; ++j) {
			lch = lch  << 1;
			rch = rch << 1;
			ltemp = s[8+expansion[i][j]/8] << (7 - expansion[i][j] % 8);
			rtemp = s[12+expansion[i][j]/8] << (7 - expansion[i][j] % 8)
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

	char leftOut[4], rightOut[4];
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
		leftOut[i] = (0x0f && (lpad >> j));
		rightOut[i] = (0x0f && (rpad >> j));
		j = j-6;
		lpad = left << (58-j);
		lpad = lpad >> (58-j);
		rpad = right << (58-j);
		rpad = rpad >> (58-j);
		leftOut[i] = (leftOut[i] << 4) | (lpad >> j);
		rightOut[i] = (rightOut[i] << 4) | (rpad >> j);
		j = j-6;
	}

	//permutation
	
}

void SPNRound(StageBits *s, StageBits *key){
	int i;

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++){
		
	}

	// Substitution

	// Permutation
}

int main(int argc, char** argv){

	// Test Vector
	StageBits s = { {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} };

	// FiestelRound(&s);

	return 0;
}