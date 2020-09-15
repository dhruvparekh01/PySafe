import functions
func = functions.Functions()


def decrypt_DES(ciphertext, key):
    ''' Function to decrypt the ciphertext using DES '''

    global func

    input_64_bits = ciphertext  #take the input hexadecimal ciphertext and convert it into binary

    permuted_64bit = func.initial_permutation(input_64_bits)  #initially permute the ciphertext

    left = permuted_64bit[:32]  #split the ciphertext into two
    right = permuted_64bit[32:]

    for i in range(16):  #16 des round involving multiple steps but in reverse order for decryption
        new_left = right
        new_right = left ^ func.round_func(right, key[15 - i]) #perform the round function
        left = new_left
        right = new_right

    right.extend(left)  #combine the two blocks
    plaintext = func.final_permutation(right)  #perform the final permutation

    return plaintext

