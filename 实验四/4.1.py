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


def pow_signed(base, exp, mod):
    if exp >= 0:
        return pow(base, exp, mod)
    return invmod(pow(base, -exp, mod), mod)


def decode_block(m):
    hex_m = f"{m:0128x}"
    prefix = hex_m[:16]
    sequence = int(hex_m[16:24], 16)
    chunk = bytes.fromhex(hex_m[-16:]).decode("latin1")
    return prefix, sequence, chunk


n0, e0, c0 = load_frame(0)
n4, e4, c4 = load_frame(4)

if n0 != n4:
    raise ValueError("Frame0 and Frame4 do not share the same modulus")

g, a, b = egcd(e0, e4)
if g != 1:
    raise ValueError("public exponents are not coprime")

m = (pow_signed(c0, a, n0) * pow_signed(c4, b, n0)) % n0
prefix, sequence, chunk = decode_block(m)

print("common modulus attack")
print("prefix   =", prefix)
print("sequence =", sequence)
print("chunk    =", chunk)
