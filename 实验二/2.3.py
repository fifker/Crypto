import base64
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def bytesxor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def aes_ecb_decrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def aes_cbc_decrypt(data, key, iv):
    out = b""
    last = iv
    for i in range(0, len(data), 16):
        block = data[i : i + 16]
        out += bytesxor(aes_ecb_decrypt(block, key), last)
        last = block
    return out


def pkcs7_unpad(data):
    return data[: -data[-1]]


data = base64.b64decode(requests.get("https://cryptopals.com/static/challenge-data/10.txt").text)
plain = pkcs7_unpad(aes_cbc_decrypt(data, b"YELLOW SUBMARINE", b"\x00" * 16)).decode(errors="ignore")
print("\n".join(plain.splitlines()[:4]))
