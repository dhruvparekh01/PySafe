def decimal_to_binary(num, in_bytes):
    arr = []
    for i in range(8):
        rem = num % 2
        arr.append(rem)
        num = num // 2

    arr.reverse()
    for i in arr:
        in_bytes.append(i)

    return in_bytes


def add_byte(in_bytes):
    """Function to add an empty byte to the parameter bit array"""
    for i in range(8):
        in_bytes.append(0)


def byte_pad(in_bytes):
    """Function to pad the input list such that its length is a multiple of 8 bytes."""

    no = len(in_bytes)
    no_of_bytes = no // 8
    rem = no_of_bytes % 8
    to_add = 8 - rem

    if to_add == 8:
        for i in range(8):
            add_byte(in_bytes)
    else:
        for i in range(to_add-1):
            add_byte(in_bytes)

        in_bytes = decimal_to_binary(to_add, in_bytes)

    return in_bytes


def remove_byte_pad(padded):
    last_byte = str(padded[len(padded)-8:])
    last_byte = last_byte[10:len(last_byte)-2]
    no_of_bits = 8 * int(str(last_byte), 2)
    unpadded = padded[:len(padded)-no_of_bits]
    return unpadded


def remove_bit_pad(padded):
    i = len(padded) - 1 - padded[::-1].index(1)
    return padded[:i]


def bit_pad(in_bits):
    l = len(in_bits)
    to_add = 8 - (l % 8)
    in_bits.append(1)
    for i in range(to_add-1):
        in_bits.append(0)

    return in_bits

