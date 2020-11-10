import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PricePrediction:
    url = "D:\Projects\ASET\price-monitoring\Python\machine_learning\Bucharest_HousePriceDataset.csv"
    column_names = ['NrCamere', 'Suprafata', 'Etaj', 'TotalEtaje', 'Sector', 'Scor', 'Pret']

    def __init__(self):
        print("init")

    def reading_data(self):
        f = open(self.url, "r")
        column_names = f.readline().replace("\n", "").replace(" ", "").split(",")
        print(column_names)
        products = []
        for line in f:
            product = list(map(float, line.replace("\n", "").split(",")))
            product[-1] = product[-1] / 1000
            products.append(product)
        return column_names, products

    def analysis(self):
        column_names, products = self.reading_data()
        for i in range(0, len(column_names)):
            print(column_names[i], min(p[i] for p in products), max(p[i] for p in products))

    def preprocessing(self):
        np.set_printoptions(precision=3, suppress=True)

        raw_dataset = pd.read_csv(self.url, names=self.column_names,
                                  na_values='?', comment='\t',
                                  sep=',', skipinitialspace=True)
        raw_dataset = raw_dataset.apply(pd.to_numeric, errors='coerce')

        dataset = raw_dataset.copy()
        print(dataset.tail())

        train_dataset = dataset.sample(frac=0.8, random_state=0)
        test_dataset = dataset.drop(train_dataset.index)

        train_features = train_dataset.copy()
        test_features = test_dataset.copy()

        train_labels = train_features.pop('Pret')
        test_labels = test_features.pop('Pret')

        return train_features, test_features, train_labels, test_labels

    def plot_surface(self, features, labels, x, y):
        plt.scatter(features['Suprafata'], labels, label='Data')
        plt.plot(x, y, color='k', label='Predictions')
        plt.xlabel('Suprafata')
        plt.ylabel('Pret')
        plt.legend()
        plt.show()

    def build_and_compile_model(self, norm):
        model = keras.Sequential([
            norm,
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
        ])

        model.compile(loss='mean_absolute_error', optimizer=tf.keras.optimizers.Adam(0.001))
        return model

    def make_model(self):
        train_features, test_features, train_labels, test_labels = self.preprocessing()

        normalizer = preprocessing.Normalization()

        normalizer.adapt(np.array(train_features))

        print(normalizer.mean.numpy())

        first = np.array(train_features[:1])

        with np.printoptions(precision=2, suppress=True):
            print('First example:', first)
            print('Normalized:', normalizer(first).numpy())

        surface = np.array(train_features['Suprafata'])

        surface_normalizer = preprocessing.Normalization(input_shape=[1, ])
        surface_normalizer.adapt(surface)

        surface_model = tf.keras.Sequential([surface_normalizer, layers.Dense(units=1)])

        surface_model.summary()

        surface_model.predict(surface[:10])

        surface_model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.1), loss='mean_absolute_error')

        history = surface_model.fit(train_features['Suprafata'], train_labels,
                                    epochs=100,
                                    # suppress logging
                                    verbose=0,
                                    # Calculate validation results on 20% of the training data
                                    validation_split=0.2)

        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        hist.tail()

        test_results = {'surface_model': surface_model.evaluate(test_features['Suprafata'], test_labels, verbose=0)}

        x = tf.linspace(0.0, 250, 251)
        y = surface_model.predict(x)

        # self.plot_surface(train_features, train_labels, x, y)

        linear_model = tf.keras.Sequential([normalizer, layers.Dense(units=1)])

        linear_model.predict(train_features[:10])

        linear_model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.1), loss='mean_absolute_error')

        history = linear_model.fit(
            train_features, train_labels,
            epochs=100,
            # suppress logging
            verbose=0,
            # Calculate validation results on 20% of the training data
            validation_split=0.2)

        test_results['linear_model'] = linear_model.evaluate(
            test_features, test_labels, verbose=0)

        surface_model = self.build_and_compile_model(surface_normalizer)

        surface_model.summary()

        surface_model.save('../machine_learning/machinelearning')

    def load_model(self):
        surface_model = keras.models.load_model('../machine_learning/machinelearning')

        surface_model.summary()

        print(type(surface_model))

        return surface_model

    def make_prediction(self, product):
        self.load_model()

        # preproces the input

        # give it to model

        # postprocess output

        return 60000


if __name__ == '__main__':
    pricePrediction = PricePrediction()
    # pricePrediction.make_model()
    pricePrediction.load_model()


