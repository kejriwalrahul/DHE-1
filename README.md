# FHE-1
Fragile Hybrid Encryption - Mach 1

## Usage (Encryption/Decryption Code)

1. Change into code directory using ```cd Code/Production/```
2. Build binaries using ```make```
3. The binary can be run using ```./bin/cbc_fhe [options]``` 

    where options can include:

        ```-e <filname>``` - file to encrpyt

        ```-d <filname>``` - file to decrpyt

        ```-o <output_file>``` - file to write output

4. Run ```make clean``` to clean working directory.


Note: There is a temporary file called fillen created to store length of file (without padding) which is required to trim off padding while decryption. Do not remove it for proper decryption.
