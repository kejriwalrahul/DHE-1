all: config.c
	gcc encrypt.c -o fhe_encrypt
	gcc decrypt.c -o fhe_decrypt

sbox.c: 
	gcc config.c

clean:
	rm -f *.out *.o fhe_decrypt fhe_encrypt