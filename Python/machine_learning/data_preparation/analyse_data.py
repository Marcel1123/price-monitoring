import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


def is_nan(x):
    return x != x


def percentage(part, whole):
    return 100 * float(part) / float(whole)


def check_furnish(features_columns, features):
    print(features_columns)
    number_of_unfurnished_under_2015 = 0
    number_of_feature_furnish = 0
    number_of_furnished = 0

    for feature in features:
        if "Unfurnished" in feature[5] and feature[2] <= 2015:
            number_of_unfurnished_under_2015 += 1
        if "urnished" in feature[5]:
            number_of_feature_furnish += 1
        if "Furnished" in feature[5]:
            number_of_furnished += 1

    print("Unfurnished, built before 2015", number_of_unfurnished_under_2015,
          percentage(number_of_unfurnished_under_2015, len(features)), "%")
    print("Buildings with furnish info", number_of_feature_furnish,
          percentage(number_of_feature_furnish, len(features)), "%")
    print("Buildings without furnish info", len(features) - number_of_feature_furnish,
          percentage(len(features) - number_of_feature_furnish, len(features)), "%")
    print("Buildings furnished from all", number_of_furnished, percentage(number_of_furnished, len(features)), "%")
    print("Buildings unfurnished", number_of_feature_furnish - number_of_furnished,
          percentage(number_of_feature_furnish - number_of_furnished, len(features)), "%")

    furnished = []
    unfurnished = []
    nan = []

    for feature in features:
        if "Furnished" in feature[5]:
            furnished.append(feature)
        if "Unfurnished" in feature[5]:
            unfurnished.append(feature)
        if "urnished" not in feature[5]:
            nan.append(feature)
    print(len(furnished), len(unfurnished), len(nan))

    # mean value of 1 m^2 in products
    def mean_(features_):
        sum_ = 0
        count_ = 0
        for feature_ in features_:
            if not is_nan(feature_[0]):
                sum_ += feature_[-1] / feature_[0]
                count_ += 1
        return sum_ / count_

    print("Mean price furnished", mean_(furnished) * 1000, " per m^2")
    print("Mean price unfurnished", mean_(unfurnished) * 1000, " per m^2")


def check_relevant_features(features_columns, features):
    X = [feature[:-2] for feature in features] # independent columns
    y = [feature[-1] for feature in features]  # target column i.e price range
    print(X, y)
    print(features_columns)
    # TODO
    # apply SelectKBest class to extract top 10 best features


