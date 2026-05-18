import hashlib
import itertools

target = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
chars = ["(", "Q", "=", "w", "i", "n", "*", "5"]

for x in itertools.permutations(chars):
    s = "".join(x)
    if hashlib.sha1(s.encode()).hexdigest() == target:
        print(s)
        break
