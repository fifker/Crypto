import random
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


random.seed(20260515)


def randbytes(n):
    return bytes([random.getrandbits(8) for _ in range(n)])


def pkcs7_pad(data, block_size=16):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data):
    return data[: -data[-1]]


def aes_cbc_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(pkcs7_pad(data)) + encryptor.finalize()


def aes_cbc_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


key = randbytes(16)
iv = randbytes(16)
prefix = b"comment1=cooking%20MCs;userdata="
suffix = b";comment2=%20like%20a%20pound%20of%20bacon"


def encrypt(user_data):
    user_data = user_data.replace(b";", b"%3B").replace(b"=", b"%3D")
    return aes_cbc_encrypt(prefix + user_data + suffix, key, iv)


def decrypt(data):
    return pkcs7_unpad(aes_cbc_decrypt(data, key, iv))


pad_len = (16 - len(prefix) % 16) % 16
payload = b"A" * (pad_len + 16)
c = bytearray(encrypt(payload))

block_id = (len(prefix) + pad_len) // 16
target = b";admin=true;AAAA"

for i in range(len(target)):
    c[(block_id - 1) * 16 + i] ^= 0x41 ^ target[i]

plain = decrypt(bytes(c))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
print(b";admin=true;" in plain)
print(plain.decode("latin1"))
