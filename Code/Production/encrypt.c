#include <stdio.h>
#include <stdlib.h>

#include "helper.h"

// 8x8 SBoxes
extern unsigned char sbox_8_8[NO_OF_SBOXES][256];
// 6x4 SBoxes
extern unsigned char sboxes_6_4[NO_OF_SBOXES][64];
// SPN Permutation
extern unsigned char spn_permutation[16][8]; 

void FiestelRoundEncrypt(StageBits *s, char key[]){
	int i,j;

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
}

void SPNRoundEncrypt(StageBits *s, StageBits *key){
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
			int bit_no  = spn_permutation[i][j] - 1;
			int bit_val = ( s->block[bit_no / 8] >> (bit_no % 8) ) & 1;
			new_s.block[i] |= bit_val << j;
		}
	}

	// Step-3: Assign result to s
	*s = new_s;	
}

void FHE_encrypt(StageBits *inp, StageBits **key_arr, char rounds[NO_OF_ROUNDS]){
	int i;
	for(i=0; i<NO_OF_ROUNDS; i++){
		// print_stage_op(inp);
		// If SPN
		if(rounds[i] == 1)
			SPNRoundEncrypt(inp, key_arr[i]);
		// If Fiestel
		else
			FiestelRoundEncrypt(inp, key_arr[i]->block);
	}
}

/*int main(int argc, unsigned char** argv){
	StageBits s = { "hello world ami" };
	StageBits k = { {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1} };
	// char rounds[] = {1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0};
	char rounds[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	// char rounds[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	StageBits **key_arr = trivial_key_expansion(&k);

	
	// int i;
	// for(i=0;i<20;i++)	print_stage_op(key_arr[i]);
	

	printf("PlainText:\n");
	print_stage_op(&s);

	FHE_encrypt(&s, key_arr, rounds);
	
	printf("CipherText:\n");
	print_stage_op(&s);

	return 0;
}
*/