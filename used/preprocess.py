import re


pre_dict = {
    "B♭": "A#",
    "D♭": "C#",
    "E♭": "D#",
    "G♭": "F#",
    "A♭": "G#",
    "on": "/",
    "On": "/",
    "N.C.": "",
    "N.C": "",
    "N.D.": "",
    "N.D": "",
    "N.C,": ""
}


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


if __name__ == "__main__":
    path = "test.txt"
    with open(path) as f:
        for L in f:
            L = L.rstrip()
            L = L.split(" ")
            modified = multiple_replace(" ".join(L[:-1]), pre_dict)  # 表記ゆれを除去
            print(modified, L[-1])
