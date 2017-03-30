all: config.c helper.h
	mkdir -p bin/
	gcc cbc_fhe.c -o bin/cbc_fhe
	# gcc encrypt.c -o fhe_encrypt
	# gcc decrypt.c -o fhe_decrypt

clean:
	rm -f *.out *.o bin/*