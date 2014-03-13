#!/usr/bin/env python

"""
Predict values for input records using the provided model.
"""

import argparse
import pickle

import numpy as np


class Predictor(object):
    def __init__(self, model_filename):
        self.model = self.load_model(model_filename)

    def load_model(self, model_filename):
        with open(model_filename, "rb") as filehandle:
            return pickle.load(filehandle)

    def predict(self, features_filename):
        data = np.loadtxt(features_filename, delimiter=",")
        return self.model.predict(data)


def write_predictions(predictions, output_filename):
    np.savetxt(output_filename, predictions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_filename",
                        help="The pickled model.")
    parser.add_argument("features_filename",
                        help="The numerical feature data.")
    parser.add_argument("output_filename",
                        help="Output predictions to this file.")

    args = parser.parse_args()

    predictor = Predictor(args.model_filename, args.features_filename,
                          args.output_filename)

    predictions = predictor.predict(args.features_filename)
    write_predictions(predictions, args.output_filename)


if __name__ == "__main__":
    main()