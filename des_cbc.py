from bitarray import bitarray
import pad
import random
import functions
import DES
import DES_decrypt


def encrypt(plaintext, key):
    """Function to encrypt binary plaintext (bitarray format) of variable length using Cipher Block Chaining mode.
        Note that iv is not provided separately as it is stored automatically in the cipher text. Therefore the user is
         not required to remember it"""

    plaintext = pad.bit_pad(plaintext)

    plaintext = pad.byte_pad(plaintext)

    iv_arr = []

    for i in range(64):
        iv_arr.append(random.randint(0, 1))  # Generate a random iv

    iv = bitarray(iv_arr)
    iv.extend(plaintext)  # append the iv at the beginning of the plaintext for further ease of calculation
    plaintext = iv

    no_of_blocks = len(plaintext) // 64

    c0 = functions.bitarr_xor(plaintext[:64], plaintext[64:128])  # initially xor'ing the iv and first block
    count = 128

    ciphertext = iv[:64]  # adding the first block of cipher text as the iv

    for i in range(no_of_blocks - 1):
        ci = DES.DES(c0, key)
        ciphertext.extend(ci)
        if count < no_of_blocks*64:
            c0 = functions.bitarr_xor(ci, plaintext[count:count+64])
            count += 64

    return ciphertext


def decrypt(ciphertext, key):
    """Function to decrypt binary plaintext (bitarray format) of variable length using Cipher Block Chaining mode.
        Note that iv is not provided separately as it is stored automatically in the cipher text. Therefore the user is
         not required to remember it"""
    plaintext = []
    plaintext = bitarray(plaintext)
    count = len(ciphertext)
    no_bytes = count // 8
    no_blocks = no_bytes // 8

    for i in range(no_blocks-1):
        pi = ciphertext[count-64:count]
        temp = DES_decrypt.decrypt_DES(pi, key)

        ci = functions.bitarr_xor(temp, ciphertext[count-128:count-64])
        ci.extend(plaintext)
        plaintext = ci
        count -= 64

    decrypted = pad.remove_byte_pad(plaintext)
    decrypted = pad.remove_bit_pad(decrypted)

    return decrypted

