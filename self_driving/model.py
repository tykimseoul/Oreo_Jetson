from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten
import numpy as np

valid_percentage = 0.2


class Model:
    def __init__(self):
        self.model = Sequential()
        self.model_name = 'model.h5'
        self.train_name = 'train.npy'

    def build(self):
        # add model layers
        self.model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28, 28, 1)))
        self.model.add(Conv2D(32, kernel_size=3, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(10, activation='softmax'))

    def load_data(self):
        train_data = np.load(self.train_name)
        indices = np.random.permutation(train_data.shape[0])
        valid_idx, train_idx = indices[:train_data.shape[0] * valid_percentage], indices[train_data.shape[0] * valid_percentage:]
        train, valid = train_data[train_idx, :], train_data[valid_idx, :]
        return np.hsplit(train, 1), np.hsplit(valid, 1)

    def train(self, data):
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(data[0][0], data[0][1], validation_data=data[1], epochs=3)

    def load_model(self):
        pass
        # self.model = keras.models.load_model(model_name)
        # self.model.summary()

    def save(self):
        self.model.save(self.model_name)

    def predict(self, depth_map):
        return self.model.predict(depth_map)


def print_result(name, result):
    if result[0] > result[1]:
        print("{0}: 1\tAbnormal: {1:.5f}".format(name.split(".")[0], result[0]))
    else:
        print("{0}: 0\tNormal: {1:.5f}".format(name.split(".")[0], result[1]))
