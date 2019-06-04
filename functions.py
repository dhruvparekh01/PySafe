import jiphy


def initial_permutation(input_64bit):  #function to initially permutate the plaintext
    ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40,
          32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63,
          55, 47, 39, 31, 23, 15, 7]

    output_64bit = []

    for i in ip:
        output_64bit.append(input_64bit[i - 1])

    return output_64bit


def round_key_generator(cipherkey_64bit):
    cipherkey_56bit = parity_drop(cipherkey_64bit)  #pass the cipherkey through a parity drop function
    left = cipherkey_56bit[:28]  #divide the key into two
    right = cipherkey_56bit[28:]

    rkey = []

    for i in range(16):
        special_round = [0, 1, 8, 15]  #define special rounds where the block is shift one position on the left
        new_left = ""  #new left is the left block to be used for the next round
        new_right = ""  #new right is the right block to be used for the next round

        if i in special_round:
            new_left = shift_one(left)  #since it is a special round, shift left by one position
            new_right = shift_one(right)
        else:
            new_left = shift_two(left)  #since it is a special round, shift left by two positions
            new_right = shift_two(right)

        new_56bit_key = new_left + new_right
        rkey.append(compression_pbox(new_56bit_key))  #pass the key through the compression pbox and add it to the roundkey array
        left = new_left
        right = new_right

    return rkey


def round_func(input_32bit, key):
    input_48bit = expansion_pbox(input_32bit)  #pass the plaintext through the expansion pbox
    output_48bit = xor(key, input_48bit)  #xor it with the key for that round
    output_32bit = sboxes(output_48bit)  #compress the 48 bits to 32 bits by passing through the s-boxes
    final_32bit_output = permutation(output_32bit)  #finally permutate the ciphertext

    return final_32bit_output


def expansion_pbox(input_32bit):
    output_48bit = []

    e = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18,
         19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]  #hard code the expansion p-box

    for i in e:
        output_48bit.append(input_32bit[i-1])  #perform the permutation bit by bit

    return output_48bit


def xor(a, b):  #make a xor function so that the program has the freedom to xor two strings/ arrays and output an array
    c = []
    for i in range(len(a)):
        if int(a[i]) ^ int(b[i]) == 1:
            c.append('1')
        else:
            c.append('0')

    return c


def sboxes(input_48bit):
    input_48bit_array = []

    for i in range(0, 48, 6):
        input_48bit_array.append(input_48bit[i:i + 6])  #create 8 blocks of 6 bit each

    output_32bit_array = []

    s = []

    '''Hard code the eight s-boxes'''
    s.append([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])
    s.append([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])
    s.append([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])
    s.append([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])
    s.append([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])
    s.append([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])
    s.append([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])
    s.append([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

    c = 0  #counter
    for i in input_48bit_array:
        row = bin_to_int(str(i[0]) + str(i[5]))  #extract the row
        column = bin_to_int_arr(i[1:5])  #extract the column

        output_32bit_array.append(int_to_bin_4bit(s[c][row][column]))
        c += 1

    return output_32bit_array


def permutation(input_bits):
    p = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13,
         30, 6, 22, 11, 4, 25]  #hard code the permutation p-box

    output_bits = []

    proper_input = []

    for i in input_bits:
        for j in i:
            proper_input.append(j)  #since the input is in blocks, this loop disintegrates the blocks for further usage

    for i in p:
        output_bits.append(str(proper_input[i - 1]))  #permutate the input

    return output_bits


def final_permutation(input_bits):
    fp = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13,
          53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]  #hard code the final-permutation p-box
    output_bits = []

    for i in fp:
        output_bits.append(input_bits[i-1])  #permutate the input

    return output_bits


def bin_to_int(s):  #function to convert binary no. to integer to give more freedom for the data types
    s2 = ''
    for i in s:
        s2 = i + s2

    n = 0
    c = 0
    for i in s2:
        n += int(i) * 2 ** c
        c += 1

    return n


def int_to_bin_4bit(n):  #function that converts the integer no. to binary in 4 bits (used for the s-boxes)
    rev = 0
    i = 0
    while n > 0:
        rem = n % 2
        rev = rem * (10 ** i) + rev
        n = int(n // 2)
        i += 1

    s = str(rev)

    if len(s) == 1:
        s = '000' + s
    elif len(s) == 2:
        s = '00' + s
    elif len(s) == 3:
        s = '0' + s
    else:
        s = s + ''

    return s


def parity_drop(input_64bit):
    pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    '''Hard code the parity drop p-box'''
    output_56bit = []

    for i in pc1:
        output_56bit.append(input_64bit[i - 1])  #perform the permutation

    return output_56bit


def shift_one(input_28bit):  #function to shift the array by one position towards the left
    output_28bit = input_28bit[1:] + input_28bit[:1]
    return output_28bit


def shift_two(input_28bit):  #function to shift the array by two positions towards the left
    output_28bit = input_28bit[2:] + input_28bit[:2]
    return output_28bit


def compression_pbox(input_56bit):
    pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47,
           55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]  #hard code the compression p-box
    output_48bit = []

    for i in pc2:
        output_48bit.append(input_56bit[i - 1])  #perform the permutation

    return output_48bit


def bin_to_int_arr(a):  #convert the input array that represents a binary number into an integer
    s = ''
    for i in a:
        s = str(i) + s

    integer = 0

    c = 0
    for i in s:
        integer += int(i) * 2 ** c
        c += 1

    return integer


def hex(b):  #function that converts binary number to hexadecimal
    blocks = []
    for i in range(0, len(b), 4):
        blocks.append(b[i:i+4])
    h = ''

    for i in blocks:
        if i == '0000':
            h += '0'
        elif i == '0001':
            h += '1'
        elif i == '0010':
            h += '2'
        elif i == '0011':
            h += '3'
        elif i == '0100':
            h += '4'
        elif i == '0101':
            h += '5'
        elif i == '0110':
            h += '6'
        elif i == '0111':
            h += '7'
        elif i == '1000':
            h += '8'
        elif i == '1001':
            h += '9'
        elif i == '1010':
            h += 'A'
        elif i == '1011':
            h += 'B'
        elif i == '1011':
            h += 'B'
        elif i == '1100':
            h += 'C'
        elif i == '1101':
            h += 'D'
        elif i == '1110':
            h += 'E'
        else:
            h += 'F'

    return h


def hex_to_bin(h):  #function to convert hexadecimal no. to binary
    b = ''
    for i in h:
        if i == '0':
            b += '0000'
        elif i == '1':
            b += '0001'
        elif i == '2':
            b += '0010'
        elif i == '3':
            b += '0011'
        elif i == '4':
            b += '0100'
        elif i == '5':
            b += '0101'
        elif i == '6':
            b += '0110'
        elif i == '7':
            b += '0111'
        elif i == '8':
            b += '1000'
        elif i == '9':
            b += '1001'
        elif i == 'A' or i == 'a':
            b += '1010'
        elif i == 'B' or i == 'b':
            b += '1011'
        elif i == 'C' or i == 'c':
            b += '1100'
        elif i == 'D' or i == 'd':
            b += '1101'
        elif i == 'E' or i == 'e':
            b += '1110'
        else:
            b += '1111'

    return b


jiphy.to.javascript(print('Hello World'))
