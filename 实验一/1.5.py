def xor(a, key):
    return bytes([a[i] ^ key[i % len(key)] for i in range(len(a))])

s = (
    "Burning 'em, if you ain't quick and nimble\n"
    "I go crazy when I hear a cymbal"
).encode()

print(xor(s, b"ICE").hex())