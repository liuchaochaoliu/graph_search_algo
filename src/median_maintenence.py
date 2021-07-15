import numpy as np
import pandas as pd
from graph_search import median_maintenence
import argparse
import time
from datetime import datetime, timedelta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    "get the sum of median values of the first n numbers when n \
    ranges from 1 to n and obtain the sum's modulo over 10000")

    parser.add_argument('--file', '-f', type=str, help='data file path')
    args = parser.parse_args()

    start = time.time()
    median_engine = median_maintenence(args.file)
    total_numbers = median_engine.n
    print(f'there are {total_numbers} numbers in the loaded file')
    modulo = median_engine.sum_median()
    print(f'the modulo of total sum of median values is {modulo}')
    print(f'the sum of the median values is {median_engine.sum}')
    end = time.time()
    time_elapsed = end - start
    print(f'the median sum experiment took \
    {timedelta(seconds=time_elapsed)}')

    