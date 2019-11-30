import numpy as np


class BOWVectorizer:
    def __init__(self, chord_stat, threshold):
        self.threshold = threshold
        self.chord_encoder = self._get_chord_encoder(chord_stat)

    def get_chord_features(self, songs):
        X = []
        features_num = len(self.chord_encoder.keys())
        for chords in [song["chords"] for song in songs]:
            x = [0] * features_num
            for chord in chords:
                if chord in self.chord_encoder.keys():
                    x[self.chord_encoder[chord]] = 1  # 回数ではなく出現したら1を入れる
            X.append(x)
        return np.array(X)

    def _get_chord_encoder(self, chord_stat):
        """chordの出現回数の統計値からchord encoderを作成する.
        threshold以下の場合はencoderに追加しない.

        {"Cadd9": 3} 的な感じ。3がonehotのindex.
        """
        chord_encoder = {}
        i = 0
        for chord, freq in chord_stat.items():
            if freq > self.threshold:
                chord_encoder[chord] = i
                i += 1
        return chord_encoder
