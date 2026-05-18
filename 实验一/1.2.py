def bytesxor(a, b):
    if len(a) > len(b):
        return bytes([x ^ y for x, y in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for x, y in zip(a, b[:len(a)])])
    
print(bytesxor(bytes.fromhex('1c0111001f010100061a024b53535009181c'), bytes.fromhex('686974207468652062756c6c277320657965')).hex())