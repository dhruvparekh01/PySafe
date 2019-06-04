import functions


def DES(plaintext, key):
    input_64bit = functions.hex_to_bin(plaintext)  #convert the hexadecimal input to binary
    cipherkey_64bit = functions.hex_to_bin(key)  #convert the hexadecimal key to binary

    permuted_plaintext = functions.initial_permutation(input_64bit)  #initially permutate the plaintext
    key = functions.round_key_generator(cipherkey_64bit)  #generate 16 round keys

    left = permuted_plaintext[:32]  #divide the plaintext into 2 blocks
    right = permuted_plaintext[32:]

    for i in range(16):  #16 des round involving multiple steps
        new_left = list(right)
        new_right = functions.xor(left, functions.round_func(right, key[i]))  #perform the round function
        right = new_right
        left = new_left

    a = list(left)
    b = list(right)
    b.extend(a)  #combine the two blocks

    ciphertext = functions.final_permutation(b)  #perform the final permutation

    output = ''
    for i in ciphertext:  #convert the ciphertext into a string
        output += i

    return functions.hex(output)

