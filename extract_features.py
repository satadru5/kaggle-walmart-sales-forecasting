#!/usr/bin/env python

"""
Extracts numerical features from the full CSV file with all data (which
contains both numerical and categorical attributes).
"""

import argparse
import csv
import datetime

import numpy as np


STORE_ID = "store_id"
TYPE = "type"
SIZE = "size"
DATE = "date"
TEMPERATURE = "temperature"
FUEL_PRICE = "fuel_price"
MARKDOWN1 = "markdown1"
MARKDOWN2 = "markdown2"
MARKDOWN3 = "markdown3"
MARKDOWN4 = "markdown4"
MARKDOWN5 = "markdown5"
CPI = "cpi"
UNEMPLOYMENT = "unemployment"
IS_HOLIDAY = "is_holiday"
WEEKLY_SALES = "weekly_sales"

FEATURES = [STORE_ID, TYPE, SIZE, DATE, TEMPERATURE, FUEL_PRICE, MARKDOWN1,
            MARKDOWN2, MARKDOWN3, MARKDOWN4, MARKDOWN5, CPI, UNEMPLOYMENT,
            IS_HOLIDAY, WEEKLY_SALES]


class NumericalFeatureExtractor(object):
    def __init__(self, input_filename):
        self.categorical_transformer = OneHotEncoder()
        self.date_transformer = DateTransformer()
        self.markdown_transformer = MarkdownTransformer()
        self.num_transformer = NumberTransformer()
        self.boolean_encoder = BooleanEncoder()

        self.feature_vectors = self.build_feature_vectors(input_filename)

    def build_feature_vectors(self, filename):
        records = []
        with open(filename, "rb") as filehandle:
            for record in csv.DictReader(filehandle, fieldnames=FEATURES):
                records.append(record)

        def get_column(column_name):
            return [record[column_name] for record in records]

        store_ids = self.num_transformer.transform(get_column(STORE_ID))
        types = self.categorical_transformer.transform(get_column(TYPE))
        sizes = self.num_transformer.transform(get_column(SIZE))
        dates = self.date_transformer.transform(get_column(DATE))
        temps = self.num_transformer.transform(get_column(TEMPERATURE))
        fuel_prices = self.num_transformer.transform(get_column(FUEL_PRICE))
        markdown1 = self.markdown_transformer.transform(get_column(MARKDOWN1))
        markdown2 = self.markdown_transformer.transform(get_column(MARKDOWN2))
        markdown3 = self.markdown_transformer.transform(get_column(MARKDOWN3))
        markdown4 = self.markdown_transformer.transform(get_column(MARKDOWN4))
        markdown5 = self.markdown_transformer.transform(get_column(MARKDOWN5))
        cpis = self.num_transformer.transform(get_column(CPI))
        unemployment = self.num_transformer.transform(get_column(UNEMPLOYMENT))
        is_holiday = self.boolean_encoder.transform(get_column(IS_HOLIDAY))
        weekly_sales = self.num_transformer.transform(get_column(WEEKLY_SALES))

        feature_vectors = [
            store_ids,
            sizes,
            dates,
            temps,
            fuel_prices,
            markdown1,
            markdown2,
            markdown3,
            markdown4,
            markdown5,
            cpis,
            unemployment,
            is_holiday,
            weekly_sales
        ]

        for i in xrange(types.shape[1]):
            feature_vectors.insert(1 + i, types[:, i])

        return np.column_stack(feature_vectors)

    def get_feature_vectors(self):
        return self.feature_vectors

    def write_feature_vectors(self, output_filename):
        np.savetxt(output_filename, self.feature_vectors, delimiter=",")


class DateTransformer(object):
    def transform(self, date_strings):
        date_format = "%Y-%m-%d"
        dates = set()

        for date_str in date_strings:
            dates.add(datetime.datetime.strptime(date_str, date_format))

        sorted_dates = sorted(dates)

        encodings = {}
        for i, date in enumerate(sorted_dates):
            encodings[date.strftime(date_format)] = i

        numerical = np.zeros(len(date_strings))
        for i, date_str in enumerate(date_strings):
            numerical[i] = encodings[date_str]

        return numerical


class OneHotEncoder(object):
    def transform(self, values):
        encodings = {}
        index = 0

        for value in values:
            if value not in encodings:
                encodings[value] = index
                index += 1

        numerical = np.zeros((len(values), index))

        for i, value in enumerate(values):
            numerical[i][encodings[value]] = 1

        return numerical


class MarkdownTransformer(object):
    def transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            if value == "NA":
                new_values[i] = 0
            else:
                new_values[i] = value

        return new_values


class NumberTransformer(object):
    def transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            new_values[i] = float(value)

        return new_values


class BooleanEncoder(object):
    def transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            if value == "TRUE":
                new_values[i] = 1
            elif value == "FALSE":
                new_values[i] = 0
            else:
                raise ValueError("Must be TRUE or FALSE, but was %s" % value)

        return new_values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")

    args = parser.parse_args()

    NumericalFeatureExtractor(args.input_filename).write_feature_vectors(
        args.output_filename)


if __name__ == "__main__":
    main()
