"""データ前処理用共通部分"""

from collections import Counter
from sklearn.model_selection import train_test_split


class CommonPreprocessor:
    def __init__(self, rare_capo_list, val_rate, test_rate, split_seed):
        self.rare_capo_list = rare_capo_list
        self.val_rate = val_rate
        self.test_rate = test_rate
        self.split_seed = split_seed

    def get_song_list(self, original_path):
        with original_path.open("r") as f:
            songs = f.readlines()
        result = []
        for song in songs:
            song = song.rstrip('\n')
            divided = song.split(" ")
            song_dic = {"chords": divided[:-1], "rec_capo": divided[-1]}
            result.append(song_dic)
        return result

    def remove_rare_capo_song(self, songs):
        """rare_capo_listに入っているのデータを除去する."""
        removed = []
        for song in songs:
            if song["rec_capo"] not in self.rare_capo_list:
                removed.append(song)
        return removed

    def split_dataset(self, songs):
        songs_train_val, songs_test = train_test_split(songs, test_size=self.test_rate, random_state=self.split_seed)
        songs_train, songs_val = train_test_split(songs, test_size=self.val_rate, random_state=self.split_seed)
        return songs_train, songs_val, songs_test

    def retrieve_chord_stat(self, songs):
        chord_dict = Counter()
        for song in songs:
            for chord in song["chords"]:
                chord_dict[chord] += 1
        return chord_dict

    def retrieve_capo_stat(self, songs):
        capo_dict = Counter()
        for song in songs:
            capo_dict[song["rec_capo"]] += 1
        return capo_dict
