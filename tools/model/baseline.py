from scipy.stats import rankdata
import numpy as np
from scipy.sparse import csr_matrix


class BaselineModel:
    def __init__(self, generator, capo_stat_train):
        self.generator = generator
        self.capo_stat_train = capo_stat_train

    def get_baseline_matrix(self, X):
        songs_num = X.toarray().shape[0]
        """trainでおすすめcapoだった回数に比例して予測を行う.baseline用"""
        hoge = self.generator.capo_encoder.transform(
            [{"rec_capo": capo} for capo in self.capo_stat_train.keys()]).toarray()
        counts = np.array([count for count in self.capo_stat_train.values()])
        predicted_rank = rankdata(-counts)
        return np.array([sum(hoge * predicted_rank)]).repeat(songs_num, axis=0)

    def predict_rank(self, test_interactions, train_interactions=None, item_features=None, user_features=None, num_threads=1, check_intersections=True):
        X_array = test_interactions.toarray()
        predict_mat = self.get_baseline_matrix(test_interactions)
        return csr_matrix(predict_mat * X_array, dtype=np.float32)
