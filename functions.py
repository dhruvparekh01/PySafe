import bitarray
import s_box_bin


class Functions:
    def __init__(self):
        self.ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6,
                   64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53,
                   45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

        self.e = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18,
                  19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]  # hard code the
        # expansion p-box

        self.s = s_box_bin.s_boxes()

        self.p = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13,
                  30, 6, 22, 11, 4, 25]  # hard code the permutation p-box

        self.fp = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5,
                   45, 13,53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10,
                   50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]  # hard code the final-permutation p-box

    def initial_permutation(self, input_64bit):  # function to initially permutate the plaintext

        output_64bit = bitarray.bitarray([])

        for i in self.ip:
            output_64bit.append(input_64bit[i - 1])

        return output_64bit

    def round_func(self, input_32bit, key):
        input_48bit = self.expansion_pbox(input_32bit)  # pass the plaintext through the expansion pbox
        output_48bit = key ^ input_48bit  # xor it with the key for that round
        output_32bit = self.sboxes(output_48bit)  # compress the 48 bits to 32 bits by passing through the s-boxes
        final_32bit_output = self.permutation(output_32bit)  # finally permutate the ciphertext

        return final_32bit_output

    def expansion_pbox(self, input_32bit):
        output_48bit = bitarray.bitarray([])

        for i in self.e:
            output_48bit.append(input_32bit[i-1])  # perform the permutation bit by bit

        return output_48bit

    def sboxes(self, input_48bit):
        input_48bit_array = []

        for i in range(0, 48, 6):
            input_48bit_array.append(input_48bit[i:i + 6])  # create 8 blocks of 6 bit each

        output_32bit_array = []

        c = 0  # counter
        for i in input_48bit_array:
            row = self.get_row(i)  # extract the row
            column = self.get_col(i)  # extract the column

            output_32bit_array.append(self.s[c][row][column])
            c += 1

        return output_32bit_array

    def get_row(self, bin):
        n1 = int(bin[0])
        n2 = int(bin[5])

        if n1 == 0:
            if n2 == 0:
                return 0
            else:
                return 1
        else:
            if n2 == 0:
                return 2
            else:
                return 3

    def get_col(self, bin):
        n1 = int(bin[1])
        n2 = int(bin[2])
        n3 = int(bin[3])
        n4 = int(bin[4])

        s = str(n1) + str(n2) + str(n3) + str(n4)

        num = int(s, 2)
        return num

    def permutation(self, input_bits):
        output_bits = []
        output_bits = bitarray.bitarray(output_bits)

        proper_input = []
        proper_input = bitarray.bitarray(proper_input)

        for i in input_bits:
            for j in i:
                proper_input.append(j)  # since the input is in blocks, this loop disintegrates the blocks for further
                # usage

        for i in self.p:
            output_bits.append(proper_input[i - 1])  # permutate the input

        return output_bits

    def final_permutation(self, input_bits):
        output_bits = []
        output_bits = bitarray.bitarray(output_bits)

        for i in self.fp:
            output_bits.append(input_bits[i-1])  # permutate the input

        return output_bits

