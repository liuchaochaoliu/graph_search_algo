import numpy as np
import pandas as pd
from graph_search import two_sum
import argparse
import time
from datetime import datetime, timedelta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    "compute the number of target values t such that t can be the sum \
        of two distinc numbers x and y")

    parser.add_argument('--file', '-f', type=str, help='data file path')
    args = parser.parse_args()
    lower_bound, upper_bound = -10000, 10000
    # lower_bound, upper_bound = 3, 10
    start = time.time()
    two_sum_engine = two_sum(args.file)
    total_numbers = two_sum_engine.n
    print(f'there are {total_numbers} numbers in the loaded file')
    two_sum_engine.find_target_value(lower_bound, upper_bound)
    end = time.time()
    time_elapsed = end - start
    print(f'the 2-sum experiment took {timedelta(seconds=time_elapsed)}')

    