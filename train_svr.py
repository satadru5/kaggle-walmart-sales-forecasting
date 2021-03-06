#!/usr/bin/env python

"""
Trains a SVR classifier.  SVR is support vector machine for regression
tasks.
"""

import argparse
import pickle

import numpy as np
from sklearn.svm import SVR


def train_model(features_filename):
    training_data = np.loadtxt(features_filename, delimiter=",")

    model = SVR(C=1.0, epsilon=0.1, kernel="linear")
    model.fit(training_data[:, :-1], training_data[:, -1])

    return model


def save_model(model, model_filename):
    with open(model_filename, "wb") as filehandle:
        pickle.dump(model, filehandle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("features_filename",
                        help="The name of the file containing numerical "
                             "attributes which can be loaded into a Numpy "
                             "array.")
    parser.add_argument("model_filename",
                        help="The file to save the trained model to.")

    args = parser.parse_args()

    model = train_model(args.features_filename)
    save_model(model, args.model_filename)


if __name__ == "__main__":
    main()
