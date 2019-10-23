#! /home/pavlo/Projects/linear_regression/venv/bin/python
import shelve
from termcolor import colored


def predict_single_price(t0, t1, miles): return t0 + t1 * miles


def main(t0, t1):
    while True:
        mileage = input(colored("Mileage: ", 'yellow'))
        if mileage.isalnum():
            print(predict_single_price(t0, t1, int(mileage)))
        else:
            print("Please, put a number!")


if __name__ == "__main__":
    try:
        with shelve.open('teta') as s:
            t0 = s['t0']
            t1 = s['t1']
    except KeyError:
        print(colored("PLease, train model first!", 'red'))
        exit()
    try:
        main(t0, t1)
    except KeyboardInterrupt:
        print("\nFinished!")
