import numpy as np


class FrequencyVectorizer:
    def __init__(self, chord_stat, threshold, token):
        self.threshold = threshold
        self.token = token
        self.chord_encoder = self._get_chord_encoder(chord_stat)

    def tokenize_rare_chord(self, chords_list):
        """低頻度なコードを指定したtokenに変換する."""
        result = []
        for chords in chords_list:
            result_inner = []
            for i, chord in enumerate(chords):
                if chord not in self.chord_encoder.keys():
                    result_inner.append(self.token)
                else:
                    result_inner.append(chord)
            result.append(result_inner)
        return result

    def _get_chord_encoder(self, chord_stat):
        """chordの出現回数の統計値からchord encoderを作成する.
        threshold以下の場合はencoderに追加しないで、Tokenにする.

        {"Cadd9": 3} 的な感じ。3がonehotのindex.
        """
        chord_encoder = {}
        i = 0
        for chord, freq in chord_stat.items():
            if freq > self.threshold:
                chord_encoder[chord] = i
                i += 1
        chord_encoder[self.token] = i
        return chord_encoder

    def count_and_normalize_chord_features(self, tokenized):
        """tokenizeされたコードのlistから頻度ベクトルを作成する."""
        X = []
        features_num = len(self.chord_encoder)
        for chords in tokenized:
            x = [0] * features_num
            for chord in chords:
                x[self.chord_encoder[chord]] += 1
            x = np.array(x)
            X.append(x / sum(x))
        return np.array(X)

    def get_chord_features(self, chords_list):
        tokenized = self.tokenize_rare_chord(chords_list)
        X = self.count_and_normalize_chord_features(tokenized)
        return X
