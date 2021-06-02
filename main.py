import numpy as np
import pandas as pd
from graph_search import dfs
import argparse
import time
from datetime import datetime, timedelta

def run_dfs_exp(data_file_path):
	
	# 1.0 import graph from txt file
	g_df = pd.read_csv(data_file_path,  sep=' ', header=None)
	if len(g_df.columns) > 2:
		g_df = g_df.drop(g_df.columns[2:], axis=1)

	# 2.0 run dfs search to find scc regions
	dfs_engine = dfs(g_df)
	scc_df = dfs_engine.dfs_scc()

	# 3.0 print out the largest 5 scc regions
	scc_sizes = -np.sort(-scc_df.groupby('leader').size())
	if len(scc_sizes) >=5:
	    print(f'The largest 5 scc sizes are {scc_sizes[:5]}')
	else:
	    scc_sizes = scc_sizes.tolist() + [0]*(5-len(scc_sizes))
	    print(f'The largest 5 scc sizes are {scc_sizes}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run dfs to find scc regions')
    parser.add_argument('--file', '-f', type=str, help='data file path')
    args = parser.parse_args()

    start = time.time()
    run_dfs_exp(args.file)
    end = time.time()
    time_elapsed = end - start
    print(f'the dfs search experiment took {timedelta(seconds=time_elapsed)}')