#include <stdio.h>
#include <stdlib.h>
#include "config.c"

#define NO_OF_SBOXES 16
#define NO_OF_ROUNDS 20

// 8x8 SBoxes
extern unsigned char inv_sbox_8_8[NO_OF_SBOXES][256];

// 6x4 SBoxes
extern unsigned char sboxes_6_4[NO_OF_SBOXES][64];

// Inverse SPN Permutation
extern unsigned char inv_spn_permutation[NO_OF_SBOXES][8]; 

typedef struct {
	unsigned char block[NO_OF_SBOXES];
} StageBits;

void print_stage_op(StageBits *s){
	int i;
	for(i=0; i<NO_OF_SBOXES; i++)
		printf("0x%x, ", s->block[i]);
	printf("\n");
}

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
			int bit_no  = inv_spn_permutation[i][j] - 1;
			int bit_val = ( s->block[bit_no / 8] >> (bit_no % 8) ) & 1;
			new_s.block[i] |=  bit_val << j;
		}
	}
	
	// Step-3: Assign result to s
	*s = new_s;

	// Inverse Substitution Layer
	for(i=0; i<NO_OF_SBOXES; i++)
		s->block[i] = inv_sbox_8_8[i][s->block[i]];

	// Key Addition
	for(i=0; i<NO_OF_SBOXES; i++)
		s->block[i] ^= key->block[i]; 		
}

void FiestelRound(StageBits *s, char key[]){
	char leftHalf[6], rightHalf[6];
	char lch, rch, ltemp, rtemp, tempval;
	int i, j;

	unsigned char temp;
	//swap left half with right half of cipher text
	for (i=0; i<8; i++) {
		temp = s->block[i];
		s->block[i] = s->block[8+i];
		s->block[8+i] = temp;
	}

	// expansion of inputs
	for (i=0; i<6; ++i) {
		lch = 0;
		rch = 0;
		for (j=0; j<8; ++j) {
			lch = lch  << 1;
			rch = rch << 1;
			tempval = expansion[i][j]-1;
			ltemp = s->block[8+tempval/8] << (7 - tempval % 8);
			rtemp = s->block[12+tempval/8] << (7 - tempval % 8);
			lch = lch | (ltemp >> 7);
			rch = rch | (rtemp >> 7);
		}
		leftHalf[i] = lch;
		rightHalf[i] = rch;
	}

	//key mixing
	for (i=0; i<6; ++i) {
		leftHalf[i] ^= key[i];
		rightHalf[i] ^= key[i+6];
	}

	unsigned char out[8];
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
	j=42;
	for (i=0; i<4; ++i) {
		lpad = left & (0xffffffffffffffff >> (58-j));
		rpad = rpad & (0xffffffffffffffff >> (58-j));
		out[i] = (0x0f & (lpad >> j));
		out[4+i] = (0x0f & (rpad >> j));
		j = j-6;
		lpad = left & (0xffffffffffffffff >> (58-j));
		rpad = rpad & (0xffffffffffffffff >> (58-j));
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
	// printf("%lu\n",lpad);
	for (i=0; i<2; ++i) {
		for (j=0; j<8; j++) {
			lch = out[4+ (i<<2) + j/8] << j;
			lch = lch >> (7-j);
			rpad = lpad;
			rpad = rpad << (64 - fperm[2+i][j]);
			rpad = lch | (rpad >> (fperm[2+i][j] - 1));
			lpad = lpad | (rpad << (fperm[2+i][j] - 1));
		}
	}
	// printf("%lu\n",lpad);
	for (i=7; i>=0; --i) {
		out[i] = lpad;
		lpad = lpad >> 8;
	}

	//xor lefthalf with fiestel output
	for (i=0; i<8; ++i) {
		out[i] ^= s->block[i];
	}
	for (i=0; i<8; ++i) {
		s->block[i] = s->block[8+i];
		s->block[8+i] = out[i];
	}


	for (i=0; i<8; i++) {
		temp = s->block[i];
		s->block[i] = s->block[8+i];
		s->block[8+i] = temp;
	}
}

void FHE_decrypt(StageBits *out, StageBits **key_arr_inv, char rounds[NO_OF_ROUNDS]){
	int i;
	for(i=0; i<NO_OF_ROUNDS; i++){
		// print_stage_op(key_arr_inv[NO_OF_ROUNDS -1 - i]);
		// If SPN
		if(rounds[i] == 1)
			SPNRound(out, key_arr_inv[NO_OF_ROUNDS -1 - i]);
		// If Fiestel
		else
			FiestelRound(out, key_arr_inv[NO_OF_ROUNDS -1 - i]->block);
	}
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

int main(int argc, unsigned char** argv){
	
	// SPN Test Vector
	StageBits s = { 0x61, 0xf9, 0xfa, 0x7e, 0x1b, 0x56, 0x62, 0xab, 0xbb, 0xd4, 0xcd, 0x6f, 0x20, 0xbd, 0x4, 0x7 };
	StageBits k = { {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1} };
	char rounds[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	// char rounds[] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1};

	StageBits **key_arr = trivial_key_expansion(&k);

	printf("CipherText: \n");
	print_stage_op(&s);

	FHE_decrypt(&s, key_arr, rounds);

	printf("PlainText: \n");
	print_stage_op(&s);

	return 0;
}