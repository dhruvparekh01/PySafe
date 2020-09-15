import functions
import bitarray
# import progressbar
import multiprocessing_encrypt as a

obj = functions.Functions()


def des(input_64bit, key):
    # input_64bit = functions.hex_to_bin(plaintext)  #convert the hexadecimal input to binary
    # cipherkey_64bit = functions.hex_to_bin(key)  #convert the hexadecimal key to binary

    global obj

    permuted_plaintext = obj.initial_permutation(input_64bit)  # initially permutate the plaintext

    left = permuted_plaintext[:32]  # divide the plaintext into 2 blocks
    right = permuted_plaintext[32:]

    for i in range(16):  # 16 des round involving multiple steps
        new_left = right
        new_right = left ^ obj.round_func(right, key[i])  # perform the round function
        right = new_right
        left = new_left

    right.extend(left)  # combine the two blocks

    ciphertext = obj.final_permutation(right)  # perform the final permutation

    return ciphertext

