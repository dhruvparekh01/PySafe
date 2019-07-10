import numpy as np
from bitarray import bitarray
import des_cbc

# File names
in_name = 'forms_encrypted.png'
out_name = 'forms2.png'

# Read data and convert to a list of bits
in_bytes = np.fromfile(in_name, dtype="uint8")
in_bits = np.unpackbits(in_bytes)
bit_list = in_bits.tolist()
print('Please wait! Getting binary data from file...')
plaintext = bitarray(bit_list)

key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

key = bitarray(key)

print('Encrypting...')
ciphertext = des_cbc.decrypt(plaintext, key)


print('Converting back to original format...')

ciphertext_list = ciphertext.tolist()
out_bytes = np.packbits(ciphertext_list)
out_bytes.tofile(out_name)

print('Done!')

