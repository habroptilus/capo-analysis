from sklearn.feature_extraction import DictVectorizer


class InteractionMatrixGenerator:
    def __init__(self, test_rate):
        self.test_rate = test_rate
        self.capo_encoder = DictVectorizer()

    def generate_matrix(self, songs):
        X = self.capo_encoder.fit_transform(
            [{"rec_capo": song["rec_capo"]} for song in songs])
        return X.toarray()

    def generate_matrices(self, songs):
        X = self.generate_matrix(songs)
        X_train = X.copy()
        X_test = X.copy()
        test_size = int(len(X) * self.test_rate)
        X_test[:-test_size, :] = 0
        X_train[-test_size:, :] = 0
        return X_train, X_test
