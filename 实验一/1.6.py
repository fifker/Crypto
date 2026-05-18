import base64
import requests


def score(s):
    ans = 0
    for c in s.lower():
        if c in b" etaoinshrdlu":
            ans += 2
        elif 32 <= c <= 126:
            ans += 1
        else:
            ans -= 5
    return ans


def hamming(a, b):
    return sum((x ^ y).bit_count() for x, y in zip(a, b))


def one_byte_xor(s):
    best = None
    for i in range(256):
        x = bytes([c ^ i for c in s])
        cur = score(x)
        if best is None or cur > best[0]:
            best = (cur, i, x)
    return best


data = base64.b64decode(requests.get("https://cryptopals.com/static/challenge-data/6.txt").text)
cand = []

for keysize in range(2, 41):
    blocks = [data[i : i + keysize] for i in range(0, keysize * 8, keysize)]
    if len(blocks[-1]) < keysize:
        continue
    dist = 0
    for i in range(len(blocks) - 1):
        dist += hamming(blocks[i], blocks[i + 1]) / keysize
    cand.append((dist / (len(blocks) - 1), keysize))

best = None

for _, keysize in sorted(cand)[:5]:
    key = b""
    for i in range(keysize):
        block = bytes([data[j] for j in range(i, len(data), keysize)])
        key += bytes([one_byte_xor(block)[1]])
    plain = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    cur = score(plain)
    if best is None or cur > best[0]:
        best = (cur, key, plain)

print(best[1].decode())
print("\n".join(best[2].decode(errors="ignore").splitlines()[:4]))
