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


best = None
data = requests.get("https://cryptopals.com/static/challenge-data/4.txt").text.splitlines()

for line_number, line in enumerate(data, 1):
    s = bytes.fromhex(line)
    for i in range(256):
        x = bytes([c ^ i for c in s])
        cur = score(x)
        if best is None or cur > best[0]:
            best = (cur, line_number, i, x)

print(best[1])
print(best[2])
print(best[3].decode())