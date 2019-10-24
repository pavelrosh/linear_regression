#! /home/pavlo/Projects/linear_regression/venv/bin/python3
import shelve
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser


def regression_line(t0, t1, data): return data.apply(lambda x: t0 + t1 * x)


def visualise_regression(t0, t1, data):
    plt.plot(data['x'], data['y'], 'yo', data['x'], regression_line(t0, t1, data['x']))
    plt.show()


def visualise_data(data):
    plt.scatter(data['x'], data['y'])
    plt.show()


def train_model(data):
    x_mean = data.mean()[0]
    y_mean = data.mean()[1]

    data['x-mean'] = data['x'].apply(lambda x: x - x_mean)
    data['y-mean'] = data['y'].apply(lambda x: x - y_mean)

    data['y-mean-sq'] = data['y-mean'].apply(lambda x: x * x)
    data['x-mean-sq'] = data['x-mean'].apply(lambda x: x * x)

    data['x-mean_multiple_price-mean'] = data['x-mean'] * data['y-mean']

    km_mean_squared_sum = data['x-mean-sq'].sum()
    km_mean_multiple_price_mean_sum = data['x-mean_multiple_price-mean'].sum()

    t1 = km_mean_multiple_price_mean_sum / km_mean_squared_sum
    t0 = -1 * (t1 * x_mean) + y_mean
    data['y_regr'] = regression_line(t0, t1, data['x'])
    data['y_regr-y_mean'] = data['y_regr'].apply(lambda x: x - y_mean)
    data['y_regr-y_mean_sq'] = data['y_regr-y_mean'].apply(lambda x: x * x)
    precision = data['y_regr-y_mean_sq'].sum() / data['y-mean-sq'].sum()
    # print(precision)
    with shelve.open('teta') as s:
        s['t0'] = t0
        s['t1'] = t1
        s['precision'] = precision


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    data = pd.DataFrame(data)
    data.rename(columns={'km': 'x', 'price': 'y'}, inplace=True)
    train_model(data)
    with shelve.open('teta') as s:
        t0 = s['t0']
        t1 = s['t1']

    parser = ArgumentParser()

    parser.add_argument('-vd', '--visualise_data', action='store_true')
    parser.add_argument('-vr', '--visualise_regression', action='store_true')
    parser.add_argument('-vp', '--visualise_precision', action='store_true')
    args = parser.parse_args()

    if args.visualise_regression:
        visualise_regression(t0, t1, data)

    if args.visualise_data:
        visualise_data(data)

    if args.visualise_precision:
        with shelve.open('teta') as s:
            print(round(float(s['precision']), 2))
