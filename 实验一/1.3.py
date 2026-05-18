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


s = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
best = None

for i in range(256):
    x = bytes([c ^ i for c in s])
    cur = score(x)
    if best is None or cur > best[0]:
        best = (cur, i, x)

print(best[1])
print(best[2].decode())
