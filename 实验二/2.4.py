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


def bytesxor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def aes_cbc_encrypt(data, key, iv):
    data = pkcs7_pad(data)
    out = b""
    last = iv
    for i in range(0, len(data), 16):
        block = bytesxor(data[i : i + 16], last)
        last = aes_ecb_encrypt(block, key)
        out += last
    return out


def detect_ecb(data, block_size=16):
    blocks = [data[i : i + block_size] for i in range(0, len(data), block_size)]
    return len(blocks) != len(set(blocks))


def oracle(data):
    key = randbytes(16)
    data = randbytes(random.randint(5, 10)) + data + randbytes(random.randint(5, 10))
    if random.randint(0, 1) == 0:
        return aes_ecb_encrypt(pkcs7_pad(data), key), "ECB"
    else:
        return aes_cbc_encrypt(data, key, randbytes(16)), "CBC"


cnt = 0
for _ in range(100):
    x, mode = oracle(b"A" * 64)
    guess = "ECB" if detect_ecb(x) else "CBC"
    if guess == mode:
        cnt += 1

print(cnt)
