"""FMのlossをBPRにしたモデル.fastFMで実装."""
from sklearn.metrics import accuracy_score
from fastFM import bpr
from scipy import sparse
import numpy as np
from sklearn.preprocessing import LabelBinarizer


class FMBPR:
    def __init__(self, n_iter, rank, step_size, sampling_rate, dupulication_capo_order):
        self.model = bpr.FMRecommender(n_iter=n_iter, step_size=step_size, rank=rank)
        self.sampling_rate = sampling_rate
        self.dupulication_capo_order = dupulication_capo_order
        self.capo_encoder = None

    def fit(self, X, y):
        """
        :param X: np.arrayでchord featureのみ。複製前.
        :param y: recomennded capo. 文字列. len(X)=len(y)
        """
        X_dup = self.duplicate_add_capo_features(X)
        X_sp = sparse.csr_matrix(X_dup)
        compares = self.create_compares(y)
        return self.model.fit(X_sp, compares)

    def predict(self, X):
        """
        :param X: np.arrayでchord featureのみ。複製前.
        :param y: recomennded capo. 文字列. len(X)=len(y)
         :return e.g. np.array([["+1", "-4", "0",...],["-1", "-3", "+1",...],...])
        """
        rankings = self.predict_ranking(X)
        return np.array([ranking[0] for ranking in rankings])

    def predict_ranking(self, X):
        """入力した曲に対しておすすめcapoのランキングを返す.

         :param X: np.arrayでchord featureのみ。複製前.
         :return e.g. np.array(["+1", "-4", "0",...])
        """
        X_dup = self.duplicate_add_capo_features(X)
        X_sp = sparse.csr_matrix(X_dup)
        pred = self.model.predict(X_sp)
        reshaped = np.reshape(pred, (-1, len(self.dupulication_capo_order)))
        results = []
        for i in range(len(reshaped)):
            results.append(self.return_sorted_capo(reshaped[i]))
        return results

    def get_all_embeddings(self):
        """embeddingを全てまとめて取得"""
        return self.model.V_.T

    def get_embeddings(self):
        """学習結果としてchordとcapoのembeddingを取得"""
        embeddings = self.get_all_embeddings()
        chord_embeddings = embeddings[:-len(self.dupulication_capo_order), :]
        capo_embeddings = embeddings[-len(self.dupulication_capo_order):, :]
        return chord_embeddings, capo_embeddings

    def create_compares(self, y):
        """おすすめcapo=yを用いてcomparesを作成."""
        compares = []
        for i, rec in enumerate(y):
            pos_j = int(np.where(self.dupulication_capo_order == rec)[0])
            for j in range(len(self.dupulication_capo_order)):
                if j != pos_j:
                    compares.append([len(self.dupulication_capo_order) * i + pos_j, len(self.dupulication_capo_order) * i + j])
        compares = np.array(compares)
        index = np.random.choice(list(range(len(compares))),
                                 int(self.sampling_rate * len(compares)), replace=False)
        return compares[index]

    def return_sorted_capo(self, pred):
        """予測したscoreを元にrankingになるようにsortする."""
        index = [0] * len(self.dupulication_capo_order)
        for j, rank in enumerate(np.argsort(pred[::-1])):
            index[rank] = j
        return self.dupulication_capo_order[index]

    def evaluate_top1(self, X, y):
        """
        :param X: np.arrayでchord featureのみ。複製前.
        :param y: recomennded capo. 文字列. len(X)=len(y)
        """
        pred = self.predict(X)
        return accuracy_score(y, pred)

    def capo_onehot_encode(self, duplicated_capos):
        """文字列のcapoをonehot encoding"""
        if self.capo_encoder is None:
            self.capo_encoder = LabelBinarizer()
            return self.capo_encoder.fit_transform(duplicated_capos)
        else:
            return self.capo_encoder.transform(duplicated_capos)

    def duplicate_capos(self, n):
        """n回dupulication_capo_orderを繰り返す."""
        return np.tile(self.dupulication_capo_order, n)

    def duplicate_add_capo_features(self, X):
        """
        :param X: np.arrayでchord featureのみ。複製前.
        """
        expanded_chord_features = X.repeat(len(self.dupulication_capo_order), axis=0)
        duplicated_capos = self.duplicate_capos(len(X))
        capo_features = self.capo_onehot_encode(duplicated_capos)
        return np.concatenate([expanded_chord_features, capo_features], 1)
