import functions
import DES
import DES_decrypt


def triple_des(plaintext, k):
    input_64bit = plaintext

    '''Split the cipherkey into three '''

    cipherkey1_64bit = k[:16]
    cipherkey2_64bit = k[16:32]
    cipherkey3_64bit = k[32:48]

    ciphertext1 = DES.DES(input_64bit, cipherkey1_64bit)  #encrypt with DES using key1
    ciphertext2 = DES_decrypt.decrypt_DES(ciphertext1, cipherkey2_64bit)  #decrypt with DES using key2
    ciphertext3 = DES.DES(ciphertext2, cipherkey3_64bit)  #encrypt with DES using key3

    return ciphertext3

