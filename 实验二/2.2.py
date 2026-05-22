def pkcs7_pad(data, block_size):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len


print(pkcs7_pad(b"YELLOW SUBMARINE", 20))
