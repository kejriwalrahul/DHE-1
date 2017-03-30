#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "helper.h"
#include "encrypt.c"
#include "decrypt.c"

StageBits IV = { { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 } };

void xor_stage_bits(StageBits* xor_to, StageBits* xor_from){
	int i;
	for(i=0; i<NO_OF_SBOXES; i++){
		xor_to->block[i] ^= xor_from->block[i];
	}
}

void cbc_fhe_encrypt(FILE *in, FILE *out, StageBits *key){
	int i;
	StageBits round_bits;
	StageBits *old_cipher = &IV;
	StageBits **key_arr = trivial_key_expansion(key);
	char rounds[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};

	while(!feof(in)){
		memset(round_bits.block, 0, sizeof(char)*NO_OF_SBOXES);

		// Read 128 bit input
		for(i=0; i<NO_OF_SBOXES; i++){
			fscanf(in, "%c", &round_bits.block[i]);
			if(feof(in))	break;
		}
		
		// XOR prev cipher text
		xor_stage_bits(&round_bits, old_cipher);
		// Encrypt
		FHE_encrypt(&round_bits, key_arr, rounds);
		// Write to file
		for(i=0; i<NO_OF_SBOXES; i++){
			fprintf(out, "%c", round_bits.block[i]);
		}

		// Chain cipher text
		*old_cipher = round_bits;
	}
}

void cbc_fhe_decrypt(FILE *out, FILE *in, StageBits *key){
	int i;
	StageBits round_bits;
	StageBits *old_cipher = &IV;
	StageBits curr_cipher;
	StageBits **key_arr = trivial_key_expansion(key);
	char rounds[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};

	while(!feof(out)){
		memset(round_bits.block, 0, sizeof(char)*NO_OF_SBOXES);

		// Read 128 bit input
		for(i=0; i<NO_OF_SBOXES; i++){
			fscanf(out, "%c", &round_bits.block[i]);
			if(feof(out))	break;
		}

		// Chain cipher text
		curr_cipher = round_bits;
		
		// Decrypt
		FHE_decrypt(&round_bits, key_arr, rounds);

		// XOR prev cipher text
		xor_stage_bits(&round_bits, old_cipher);		

		// Write to file
		for(i=0; i<NO_OF_SBOXES; i++){
			fprintf(in, "%c", round_bits.block[i]);
		}

		*old_cipher = curr_cipher;
	}	
}

int main(int argc, char** argv){
	char 	is_encrypt = 0;
	char* 	filname    = "input";
	char* 	outfilname = "output";
	StageBits key = { {16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1} };
	int i;

	// Improper usage break 
	if(argc < 3){
		printf("Incorrect Usage! Usage: ./cbc_fhe <-e/-d> <filname> -o <filname>\n");
		return 1;
	}

	for(i=1; i<argc; i++){
		// Check encrypt/decrypt
		if(!strcmp("-e", argv[i])){
			is_encrypt = 1;
			filname = argv[i+1];
			i++;
		}
		else if(!strcmp("-d", argv[i])){
			is_encrypt = 0;
			filname = argv[i+1];
			i++;
		}
		else if(!strcmp("-o", argv[i])){
			outfilname = argv[i+1];
			i++;
		}
		else{
			printf("Unrecognized option! Use either -e or -d or -o");
			return 1;
		}		
	}

	FILE *in = fopen(filname, "r");
	FILE *out = fopen(outfilname, "w");

	if(!in || !out){
		printf("Unable to open files! Aborting!\n");
		return 1;
	}

	if(is_encrypt)
		cbc_fhe_encrypt(in, out, &key);
	else
		cbc_fhe_decrypt(in, out, &key);

	fclose(in);
	fclose(out);

	return 0;
}