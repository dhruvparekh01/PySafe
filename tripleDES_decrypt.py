import functions
import DES
import DES_decrypt


def triple_des_decr(ciphertext, k):
    input_64bit = ciphertext

    '''Split the cipherkey into three '''

    cipherkey1_64bit = k[:16]
    cipherkey2_64bit = k[16:32]
    cipherkey3_64bit = k[32:64]

    plaintext1 = DES_decrypt.decrypt_DES(input_64bit, cipherkey3_64bit)  #decrypt with DES using key1
    plaintext2 = DES.DES(plaintext1, cipherkey2_64bit)  #encrypt with DES using key2
    plaintext3 = DES_decrypt.decrypt_DES(plaintext2, cipherkey1_64bit)  #decrypt with DES using key3

    return plaintext3

