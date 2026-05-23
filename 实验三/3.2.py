import random
random.seed(20260515)


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - a // b * y1


def invmod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(10):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        ok = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True


def get_prime(bits):
    while True:
        x = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if is_prime(x) and x % 3 != 1:
            return x


p = 17
q = 23
e = 3
n = p * q
phi = (p - 1) * (q - 1)
d = invmod(e, phi)
m = 42
c = pow(m, e, n)
print(p, q, n, phi, d, c, pow(c, d, n))

p = get_prime(256)
q = get_prime(256)
while p == q:
    q = get_prime(256)

n = p * q
phi = (p - 1) * (q - 1)
d = invmod(3, phi)
m = int.from_bytes(b"ModernCryptography", "big")
c = pow(m, 3, n)
x = pow(c, d, n)

print(c)
print(x.to_bytes((x.bit_length() + 7) // 8, "big").decode())
