import base64
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def recover_mrz_character(mrz):
    weights = (7, 3, 1)
    values = {str(i): i for i in range(10)}
    values.update({chr(ord("A") + i): 10 + i for i in range(26)})
    values["<"] = 0

    def checksum(text):
        return sum(values[char] * weights[index % 3] for index, char in enumerate(text)) % 10

    for digit in "0123456789":
        candidate = mrz.replace("?", digit, 1)
        if checksum(candidate[21:27]) == int(candidate[27]):
            return digit
    raise ValueError("missing MRZ character not found")


def set_odd_parity(byte):
    masked = byte & 0xFE
    return masked | (0 if bin(masked).count("1") % 2 else 1)


def aes_cbc_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def strip_bac_padding(data):
    suffix = data.rstrip(b"\x00")
    if suffix.endswith(b"\x01"):
        return suffix[:-1]
    return data


mrz_partial = "12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4"
recovered_digit = recover_mrz_character(mrz_partial)
mrz_full = mrz_partial.replace("?", recovered_digit, 1)
mrz_info = mrz_full[:10] + mrz_full[13:20] + mrz_full[21:28]

k_seed = hashlib.sha1(mrz_info.encode()).digest()[:16]
raw_key = hashlib.sha1(k_seed + (1).to_bytes(4, "big")).digest()[:16]
key_enc = bytes(set_odd_parity(byte) for byte in raw_key)

ciphertext = base64.b64decode(
    "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jx"
    "aa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2N"
    "fNnWFBTXyf7SDI"
)
plaintext = strip_bac_padding(aes_cbc_decrypt(ciphertext, key_enc, b"\x00" * 16)).decode()

print(recovered_digit)
print(mrz_info)
print(key_enc.hex())
print(plaintext)
