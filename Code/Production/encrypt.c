#include <stdio.h>
#include "sbox.c"

// 8x8 SBoxes
extern char sbox_8_8[16][256];
extern char inv_sbox_8_8[16][256];

// 6x4 SBoxes
extern char sboxes_6_4[16][64];

typedef struct {
	char block[16];
} StageBits;

void FiestelRound(StageBits *s){
	
}

void SPNRound(StageBits *s){
	
}

int main(int argc, char** argv){

	// Test Vector
	StageBits s = { {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} };

	// FiestelRound(&s);

	return 0;
}