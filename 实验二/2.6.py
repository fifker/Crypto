import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


random.seed(20260515)
key = bytes([random.getrandbits(8) for _ in range(16)])


def pkcs7_pad(data, block_size=16):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data):
    return data[: -data[-1]]


def aes_ecb_encrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def aes_ecb_decrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def profile_for(email):
    email = email.replace("&", "").replace("=", "")
    return f"email={email}&uid=10&role=user".encode()


def encrypt_profile(email):
    return aes_ecb_encrypt(pkcs7_pad(profile_for(email)), key)


def decrypt_profile(data):
    s = pkcs7_unpad(aes_ecb_decrypt(data, key)).decode()
    print(s)


admin_block = encrypt_profile("A" * 10 + "admin" + chr(11) * 11)[16:32]
base = encrypt_profile("A" * 13)
decrypt_profile(base[:32] + admin_block)
