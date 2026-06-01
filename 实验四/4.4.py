FRAME_TO_SEQUENCE = {
    "Frame0": 0,
    "Frame4": 0,
    "Frame3": 1,
    "Frame8": 1,
    "Frame12": 1,
    "Frame16": 1,
    "Frame20": 1,
    "Frame7": 2,
    "Frame11": 3,
    "Frame15": 4,
    "Frame19": 5,
    "Frame2": 6,
    "Frame6": 7,
    "Frame10": 8,
    "Frame14": 9,
    "Frame18": 10,
    "Frame1": 11,
    "Frame5": 12,
    "Frame9": 13,
    "Frame13": 14,
    "Frame17": 15,
}

SEQUENCE_TO_CHUNK = {
    0: "My secre",
    1: "t is a f",
    2: "amous sa",
    3: "ying of ",
    4: "Albert E",
    5: "instein.",
    6: " That is",
    7: ' "Logic ',
    8: "will get",
    9: " you fro",
    10: "m A to B",
    11: ". Imagin",
    12: "ation wi",
    13: "ll take ",
    14: "you ever",
    15: 'ywhere."',
}

print("frame -> sequence")
for frame, sequence in sorted(FRAME_TO_SEQUENCE.items(), key=lambda item: int(item[0].replace("Frame", ""))):
    print(f"{frame:>7} -> {sequence:02d} -> {SEQUENCE_TO_CHUNK[sequence]}")

message = "".join(SEQUENCE_TO_CHUNK[i] for i in range(len(SEQUENCE_TO_CHUNK)))

print("\nRecovered plaintext:")
print(message)
