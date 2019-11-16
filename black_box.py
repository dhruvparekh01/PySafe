from bitarray import bitarray
import key_scheduler
import DES

scale = 16 ## equals to hexadecimal
num_of_bits = 64

plain_hex = "FFFFFFFFFFFFFFFF11DFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
key_hex = "1111111111111111"

s = bin(int(plain_hex, scale))[2:].zfill(num_of_bits)
plaintext = s

s = bin(int(key_hex, scale))[2:].zfill(num_of_bits)
key = s

print(plaintext)
print(key)

cipherkey = key_scheduler.round_key_generator(key)

ciphertext = DES.des(plaintext, cipherkey)

s = str(ciphertext)
s2 = s[10:74]
print(hex(int(s2, 2)))

