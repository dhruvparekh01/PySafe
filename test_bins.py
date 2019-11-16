import timeit
import struct
import bitarray

mysetup = "print('Started')"


def bins(x):
    s = "{0:b}".format(x)
    s = s.zfill(9)


def fuck(bin):
    n = int(bin[0]) * 10 + int(bin[1])
    return int(str(n), 2)


def shit(bin):
    n1 = int(bin[0])
    n2 = int(bin[1])
    if n1 == '0':
        if n2 == '0':
            print('0')
        else:
            print('1')
    else:
        if n2 == 0:
            print('2')
        else:
            print('3')


def to_bin(n):  # function that converts the integer no. to binary in 4 bits (used for the s-boxes)
    rev = 0
    i = 0
    while n > 0:
        rem = n % 2
        rev = rem * (10 ** i) + rev
        n = int(n // 2)
        i += 1

    s = str(rev).zfill(4)
    # s = str(rev)


def bin_time():
    SETUP_CODE = ''' 
from __main__ import bins
from random import randint'''

    TEST_CODE = ''' 
x = randint(0, 100)
bins(x)'''

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=300,
                          number=10000)

    # priniting minimum exec. time
    print('Time 1: {}'.format(min(times)))


def tobin_time():
    SETUP_CODE = ''' 
from __main__ import to_bin
from random import randint'''

    TEST_CODE = ''' 
x = randint(0, 100)
to_bin(x)'''

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=300,
                          number=10000)

    # priniting minimum exec. time
    print('Time 2: {}'.format(min(times)))


def fuck_time():
    SETUP_CODE = ''' 
from __main__ import fuck
from random import randint'''

    TEST_CODE = ''' 
x = randint(0, 1)
y = randint(0, 1)
fuck([x,y])'''

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=300,
                          number=10000)

    # priniting minimum exec. time
    print('Time for fuck: {}'.format(min(times)))


def shit_time():
    SETUP_CODE = ''' 
from __main__ import shit
from random import randint'''

    TEST_CODE = ''' 
x = randint(0, 1)
y = randint(0, 1)
shit([x,y])'''

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=300,
                          number=10000)

    # priniting minimum exec. time
    print('Time for shit: {}'.format(min(times)))


def binary_to_int(s):  # function to convert binary no. to integer to give more freedom for the data types
    s2 = s[::-1]

    n = 0
    c = 0
    for i in s2:
        n += int(i) * 2 ** c
        c += 1

    return n


def binary_to_int2(s):  # function to convert binary no. to integer to give more freedom for the data types
    bin_str = str(s)
    print(int(bin_str, 2))


if __name__ == '__main__':
    # fuck_time()
    d = bitarray.bitarray('111')

    print(type(d))

