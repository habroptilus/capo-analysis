from sklearn.metrics import accuracy_score
from fastFM import sgd  # ,als
import numpy as np


class FMClassifier:
    def __init__(self, n_iter, rank, preprocessor):
        self.model = sgd.FMClassification(n_iter=n_iter, rank=rank)
        self.preprocessor = preprocessor

    def fit(self, X, y):
        X, y = self.preprocessor.preprocess(X, y, do_sampling=True)
        return self.model.fit(X, y)

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
        X = self.preprocessor.preprocess(X, do_sampling=False)
        pred = self.model.predict_proba(X)
        reshaped = np.reshape(pred, (-1, len(self.preprocessor.dupulication_capo_order)))
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
        chord_embeddings = embeddings[:-len(self.preprocessor.dupulication_capo_order), :]
        capo_embeddings = embeddings[-len(self.preprocessor.dupulication_capo_order):, :]
        return chord_embeddings, capo_embeddings

    def evaluate_top1(self, X, y):
        """
        :param X: np.arrayでchord featureのみ。複製前.
        :param y: recomennded capo. 文字列. len(X)=len(y)
        """
        pred = self.predict(X)
        return accuracy_score(y, pred)

    def return_sorted_capo(self, pred):
        """予測したscoreを元にrankingになるようにsortする."""
        index = [0] * len(self.preprocessor.dupulication_capo_order)
        for j, rank in enumerate(np.argsort(pred[::-1])):
            index[rank] = j
        return self.preprocessor.dupulication_capo_order[index]
