from scipy import sparse
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from numpy.random import randint


class CLSPreprocessor:
    """fastFMClassifier用のpreprocessor."""

    def __init__(self, dupulication_capo_order):
        self.dupulication_capo_order = dupulication_capo_order
        self.capo_encoder = None

    def preprocess(self, X, y=None, do_sampling=False):
        """preprocess本体.fitの時はdo_sampling=Trueを想定."""
        X = self.duplicate_add_capo_features(X)
        if y is None:
            return sparse.csr_matrix(X)
        y = self.create_labels(y)
        if do_sampling:
            X, y = self.sample_dataset(X, y)
        X = sparse.csr_matrix(X)
        return X, y

    def shuffle_samples(self, X, y):
        """samplingした後にshuffleする."""
        zipped = list(zip(X, y))
        np.random.shuffle(zipped)
        X_result, y_result = zip(*zipped)
        return np.asarray(X_result), np.asarray(y_result)

    def sample_dataset(self, X_dup, labels):
        """複製したX, yからsamplingする.正例と負例は1:1に"""
        X_dup_pos = X_dup[labels == 1]
        X_dup_neg = X_dup[labels == -1]
        diff = randint(0, len(self.dupulication_capo_order) - 1,
                       len(X_dup_neg) // (len(self.dupulication_capo_order) - 1))
        sampled_index = np.array([(len(self.dupulication_capo_order) - 1) * i for i in range(
            len(X_dup_neg) // (len(self.dupulication_capo_order) - 1))]) + diff
        X_dup_neg_sampled = X_dup_neg[sampled_index]
        assert len(X_dup_neg_sampled) == len(X_dup_pos)
        X_sampled = np.concatenate([X_dup_pos, X_dup_neg_sampled])
        y_sampled = np.concatenate(
            [np.ones(len(X_dup_pos)), -np.ones(len(X_dup_neg_sampled))])
        assert len(X_sampled) == len(y_sampled)
        return self.shuffle_samples(X_sampled, y_sampled)

    def create_labels(self, y):
        """おすすめcapo(=y)を用いてlabelsを作成.(負例はこの段階ではその他全てで作る.この後negative samplingして正例と揃える)"""
        labels = []
        for rec in y:
            pos_j = int(np.where(self.dupulication_capo_order == rec)[0])
            for j in range(len(self.dupulication_capo_order)):
                if j != pos_j:
                    labels.append(-1)
                else:
                    labels.append(1)
        return np.array(labels)

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
        expanded_chord_features = X.repeat(
            len(self.dupulication_capo_order), axis=0)
        duplicated_capos = self.duplicate_capos(len(X))
        capo_features = self.capo_onehot_encode(duplicated_capos)
        return np.concatenate([expanded_chord_features, capo_features], 1)
