from pathlib import Path


def project_root():
    return Path(__file__).resolve().parents[2]


def frame_dir():
    root = project_root()
    rsa_dir = next(p for p in root.iterdir() if p.is_dir() and p.name.startswith("RSA"))
    challenge_dir = next(p for p in rsa_dir.iterdir() if p.is_dir())
    return next(p for p in challenge_dir.iterdir() if p.is_dir() and "3-2" in p.name)


def load_frame(frame_id):
    raw = (frame_dir() / f"Frame{frame_id}").read_text().strip()
    n = int(raw[:256], 16)
    e = int(raw[256:512], 16)
    c = int(raw[512:], 16)
    return n, e, c


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - a // b * y1


def invmod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % m


def crt(items):
    mod_all = 1
    for _, n in items:
        mod_all *= n

    value = 0
    for a, n in items:
        part = mod_all // n
        value = (value + a * part * invmod(part, n)) % mod_all
    return value


def iroot(n, k):
    lo = 0
    hi = 1 << ((n.bit_length() + k - 1) // k)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid**k < n:
            lo = mid + 1
        else:
            hi = mid
    return lo, lo**k == n


def decode_block(m):
    hex_m = f"{m:0128x}"
    prefix = hex_m[:16]
    sequence = int(hex_m[16:24], 16)
    chunk = bytes.fromhex(hex_m[-16:]).decode("latin1")
    return prefix, sequence, chunk


frame_ids = [3, 8, 12, 16, 20]
items = []

for frame_id in frame_ids:
    n, e, c = load_frame(frame_id)
    if e != 5:
        raise ValueError(f"Frame{frame_id} is not an e=5 frame")
    items.append((c, n))

combined = crt(items)
m, exact = iroot(combined, 5)
if not exact:
    raise ValueError("broadcast attack failed")

prefix, sequence, chunk = decode_block(m)

print("Hastad broadcast attack (e = 5)")
print("prefix   =", prefix)
print("sequence =", sequence)
print("chunk    =", chunk)
