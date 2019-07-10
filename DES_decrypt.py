import functions


def decrypt_DES(ciphertext, k):
    '''Function to decrypt the ciphertext using DES'''

    input_64_bits = ciphertext  #take the input hexadecimal ciphertext and convert it into binary
    cipherkey_64bit = k  #do the same with the cipherkey

    permuted_64bit = functions.initial_permutation(input_64_bits)  #initially permute the ciphertext

    key = functions.round_key_generator(cipherkey_64bit)  #generate the 16 round keys

    left = permuted_64bit[:32]  #split the ciphertext into two
    right = permuted_64bit[32:]

    for i in range(16):  #16 des round involving multiple steps but in reverse order for decryption
        new_left = right
        new_right = functions.bitarr_xor(left, functions.round_func(right, key[15-i]))  #perform the round function
        left = new_left
        right = new_right

    right.extend(left)  #combine the two blocks
    plaintext = functions.final_permutation(right)  #perform the final permutation

    return plaintext

