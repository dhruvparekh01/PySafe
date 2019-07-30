import hashlib


def hash_pass(password):
    str = password

    res = hashlib.sha256(str.encode())
    hex_res = res.hexdigest()
    result = bin(int(hex_res, 16))[2:].zfill(256)

    return result[:64]

