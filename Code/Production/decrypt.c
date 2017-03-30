#include <stdio.h>
#include <stdlib.h>

#include "helper.h"

// 8x8 SBoxes
extern unsigned char inv_sbox_8_8[NO_OF_SBOXES][256];
// 6x4 SBoxes
extern unsigned char sboxes_6_4[NO_OF_SBOXES][64];
// Inverse SPN Permutation
extern unsigned char inv_spn_permutation[NO_OF_SBOXES][8]; 

void SPNRoundDecrypt(StageBits *s, StageBits *key){
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

void FiestelRoundDecrypt(StageBits *s, char key[]){
	int i, j;

	//swap left half with right half of cipher text
	unsigned char temp;
	for (i=0; i<8; i++) {
		temp = s->block[i];
		s->block[i] = s->block[8+i];
		s->block[8+i] = temp;
	}

	StageBits result;
	for(i=0; i<NO_OF_SBOXES/2; i++)
		result.block[i] = s->block[i+NO_OF_SBOXES/2];
	
	// Expand Input
	unsigned long expansionLeft = 0;
	for(i=0; i < 48; i++){
		int bit_no  =  64 + expansion[i] - 1;
		int bit_val = (s->block[bit_no/8] >> (7-bit_no%8)) & 1;
		expansionLeft |= bit_val << (47-i);
	}

	unsigned long expansionRight = 0;
	for(i=0; i < 48; i++){
		int bit_no  =  96 + expansion[i] - 1;
		int bit_val = (s->block[bit_no/8] >> (7-bit_no%8)) & 1;
		expansionRight |= bit_val << (47-i);
	}

	// XOR Key
	for(i=0; i<NO_OF_SBOXES/2; i++)
		expansionLeft = expansionLeft ^ (((unsigned long)(key[i] & 0x3F)) << 6*(NO_OF_SBOXES/2 -1 - i));

	for(i=NO_OF_SBOXES/2,j=42; i<NO_OF_SBOXES; i++,j-=6)
		expansionRight = expansionRight ^ (((unsigned long)(key[i] & 0x3F)) << j);
	
	// SBox Substitution
	int max_offset = (NO_OF_SBOXES/2 - 1)*6;
	for(i=0; i<NO_OF_SBOXES/4; i++){
		s->block[8+i/2]  = 0;
		s->block[8+i/2]  = sboxes_6_4[2*i  ][(expansionLeft >> (max_offset-6*(2*i)))  & 0x3F] << 4;
		s->block[8+i/2] |= sboxes_6_4[2*i+1][(expansionLeft >> (max_offset-6*(2*i+1))) & 0x3F];
	}

	for(i=0; i<NO_OF_SBOXES/4; i++){
		s->block[12+i/2]  = 0;
		s->block[12+i/2]  = sboxes_6_4[8+2*i  ][(expansionRight >> (max_offset-6*(2*i)))  & 0x3F] << 4;
		s->block[12+i/2] |= sboxes_6_4[8+2*i+1][(expansionRight >> (max_offset-6*(2*i+1))) & 0x3F];		
	}
	
	// Permutation
	for(i=NO_OF_SBOXES/2; i<(3*NO_OF_SBOXES)/4; i++){
		result.block[i] = 0;
		for(j=0; j<8; j++){
			int bit_no  = fperm[i-8][j] - 1 + 64; 
			int bit_val = (s->block[bit_no/8] >> (bit_no%8)) & 1;
			result.block[i] |= bit_val << j;
		}
	}

	for(i=(3*NO_OF_SBOXES)/4; i<NO_OF_SBOXES; i++){
		result.block[i] = 0;
		for(j=0; j<8; j++){
			int bit_no  = fperm[i-8][j] - 1 + 96; 
			int bit_val = (s->block[bit_no/8] >> (bit_no%8)) & 1;
			result.block[i] |= bit_val << j;
		}
	}

	// XOR Left half
	for(i=0; i<NO_OF_SBOXES/2; i++)
		result.block[i + NO_OF_SBOXES/2] ^= s->block[i]; 

	*s = result;

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
			SPNRoundDecrypt(out, key_arr_inv[NO_OF_ROUNDS -1 - i]);
		// If Fiestel
		else
			FiestelRoundDecrypt(out, key_arr_inv[NO_OF_ROUNDS -1 - i]->block);
	}
}

/*
int main(int argc, unsigned char** argv){
	
	// SPN Test Vector
	StageBits s = { 0x3b, 0xd4, 0x59, 0x6f, 0x6f, 0xb8, 0x77, 0xff, 0x50, 0xc9, 0x71, 0x3, 0x70, 0x76, 0x6e, 0x31 };
	// StageBits s = { 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6e, 0x72, 0x6c, 0x64, 0x20, 0x70, 0x72, 0x6f, 0x20 };
	StageBits k = { {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1} };
	// char rounds[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	char rounds[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	// char rounds[] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1};

	StageBits **key_arr = trivial_key_expansion(&k);

	printf("CipherText: \n");
	print_stage_op(&s);

	FHE_decrypt(&s, key_arr, rounds);

	printf("PlainText: \n");
	print_stage_op(&s);
	printf("%s\n", s.block);
	return 0;
}
*/