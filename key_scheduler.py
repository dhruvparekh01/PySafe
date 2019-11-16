import bitarray

special_round = [0, 1, 8, 15]  # define special rounds where the block is shift one position on the left

pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
               63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47,
               55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]  #hard code the compression p-box


def round_key_generator(cipherkey_64bit):
    cipherkey_56bit = parity_drop(cipherkey_64bit)  # pass the cipherkey through a parity drop function
    left = cipherkey_56bit[:28]  # divide the key into two
    right = cipherkey_56bit[28:]

    rkey = []
    # rkey = bitarray.bitarray(rkey)

    for i in range(16):
        new_left = ""  # new left is the left block to be used for the next round
        new_right = ""  # new right is the right block to be used for the next round

        if i in special_round:
            new_left = shift_one(left)  # since it is a special round, shift left by one position
            new_right = shift_one(right)
        else:
            new_left = shift_two(left)  # since it is a special round, shift left by two positions
            new_right = shift_two(right)

        new_56bit_key = new_left + new_right
        rkey.append(compression_pbox(new_56bit_key))
        left = new_left
        right = new_right

    return rkey


def shift_one(input_28bit):
    output_28bit = input_28bit[1:] + input_28bit[:1]
    return output_28bit


def shift_two(input_28bit):
    output_28bit = input_28bit[2:] + input_28bit[:2]
    return output_28bit


def parity_drop(input_64bit):
    input_64bit = bitarray.bitarray(input_64bit)
    output_56bit = []
    output_56bit = bitarray.bitarray(output_56bit)

    for i in pc1:
        output_56bit.append(input_64bit[i - 1])

    return output_56bit


def compression_pbox(input_56bit):
    output_48bit = []
    output_48bit = bitarray.bitarray(output_48bit)

    for i in pc2:
        output_48bit.append(input_56bit[i - 1])  # perform the permutation

    return output_48bit

