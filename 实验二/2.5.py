import base64
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


random.seed(20260515)


def randbytes(n):
    return bytes([random.getrandbits(8) for _ in range(n)])


def pkcs7_pad(data, block_size=16):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len


def aes_ecb_encrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def block_size(oracle):
    n = len(oracle(b""))
    for i in range(1, 64):
        m = len(oracle(b"A" * i))
        if m > n:
            return m - n


unknown = base64.b64decode(
    b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    b"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    b"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    b"YnkK"
)
key = randbytes(16)


def oracle(data):
    return aes_ecb_encrypt(pkcs7_pad(data + unknown), key)


bs = block_size(oracle)
ans = b""

for _ in range(len(oracle(b""))):
    pad = b"A" * (bs - 1 - len(ans) % bs)
    block_id = len(ans) // bs
    target = oracle(pad)[block_id * bs : (block_id + 1) * bs]
    d = {}
    for i in range(256):
        x = oracle(pad + ans + bytes([i]))[block_id * bs : (block_id + 1) * bs]
        d[x] = i
    if target not in d:
        break
    ans += bytes([d[target]])

print(ans.decode().rstrip("\x01"))
