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
prefix = randbytes(random.randint(5, 32))


def oracle(data):
    return aes_ecb_encrypt(pkcs7_pad(prefix + data + unknown), key)


bs = block_size(oracle)
pos = None

for i in range(bs * 2):
    x = oracle(b"A" * i + b"B" * (bs * 2))
    blocks = [x[j : j + bs] for j in range(0, len(x), bs)]
    for j in range(len(blocks) - 1):
        if blocks[j] == blocks[j + 1]:
            pos = (i, j)
            break
    if pos is not None:
        break

pad_len, block_id = pos
pad = b"A" * pad_len
ans = b""

for _ in range(len(oracle(b""))):
    short = bs - 1 - len(ans) % bs
    now_block = block_id + len(ans) // bs
    target = oracle(pad + b"A" * short)[now_block * bs : (now_block + 1) * bs]
    d = {}
    for i in range(256):
        x = oracle(pad + b"A" * short + ans + bytes([i]))[now_block * bs : (now_block + 1) * bs]
        d[x] = i
    if target not in d:
        break
    ans += bytes([d[target]])

print(block_id * bs - pad_len)
print(ans.decode().rstrip("\x01"))
