import math
p = 1009
q = 3643
phi = (p - 1) * (q - 1)

best = None
ans = 0
cnt = 0

for e in range(2, phi):
    if math.gcd(e, phi) != 1:
        continue
    x = (math.gcd(e - 1, p - 1) + 1) * (math.gcd(e - 1, q - 1) + 1)
    if best is None or x < best:
        best = x
        ans = e
        cnt = 1
    elif x == best:
        ans += e
        cnt += 1

print(best)
print(cnt)
print(ans)
