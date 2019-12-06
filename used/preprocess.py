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
    "N.C,": "",
    "Im": "",
    "N,C.": "",
    ")": "",
    "(": "",
    "Ed": "",
    "SUS": "sus",
    "Sus": "sus",
    "D7何も見えGm": "",
    "Add": "add",
    "Bm/A/愛E": "",
    "0F": "",
    "/A": "",
    '/F#': ""
}


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def remove_empty_string(chord_list):
    result = []
    for chord in chord_list:
        if len(chord) != 0:
            result.append(chord)
    return result


capo_dict = {"0": "capo0", "+1": "half_down", "-1": "capo1", "-2": "capo2",
             "-3": "capo3", "-4": "capo4", "-5": "capo5", "-6": "capo6", "-7": "capo7",
             "+2": "whole_down"}


if __name__ == "__main__":
    path = "data/raw_data_50k.txt"
    with open(path) as f:
        for L in f:
            L = L.rstrip()
            L = L.split(" ")
            if L[-1] not in capo_dict.keys():
                continue
            capo = capo_dict[L[-1]]
            modified = multiple_replace(" ".join(L[:-1]), pre_dict)  # 表記ゆれを除去
            removed = remove_empty_string(modified.split(" "))
            print(" ".join(removed), capo)
