def pkcs7_unpad(data):
    pad = data[-1]
    if pad < 1 or pad > 16 or data[-pad:] != bytes([pad]) * pad:
        raise ValueError
    return data[:-pad]


print(pkcs7_unpad(b"ICE ICE BABY\x04\x04\x04\x04"))

try:
    print(pkcs7_unpad(b"ICE ICE BABY\x05\x05\x05\x05"))
except ValueError:
    print("ValueError")

try:
    print(pkcs7_unpad(b"ICE ICE BABY\x01\x02\x03\x04"))
except ValueError:
    print("ValueError")
