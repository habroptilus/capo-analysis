import re
CHORD_LIST = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


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


def create_dict(capo):
    dict = {}
    for i in range(len(CHORD_LIST)):
        dict[CHORD_LIST[i]] = CHORD_LIST[(i + capo) % 12]
    return dict


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def create_dict(capo):
    dict = {}
    for i in reversed(range(len(CHORD_LIST))):
        dict[CHORD_LIST[i]] = CHORD_LIST[(i - capo) % 12]
    return dict


dicts = {}
for i in range(-9, 3):
    dicts[int(i)] = create_dict(i)


N = 40001
for i in range(N):
    L = input().split(" ")
    try:
        capo = int(L.pop())
    except Exception as e:
        continue
    modified = multiple_replace(" ".join(L), pre_dict)
    modified = multiple_replace(modified, dicts[capo])
    print(modified, capo)
