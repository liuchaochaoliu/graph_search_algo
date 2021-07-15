import numpy as np
import pandas as pd
from graph_search import shortest_path
import argparse
import time
from datetime import datetime, timedelta

def run_sp_exp(data_file_path, selected_node, source_vertex=1):
    # 1.0 run dijkstra to find shortest paths
    sp_engine = shortest_path(data_file_path)
    sp_engine.sp_search(source_vertex=source_vertex)

    # 2.0 return the shortest paths for the selected nodes
    selected_idx = [item-1 for item in selected_nodes]
    distance_list = [sp_engine.A[item] for item in selected_idx]
    path_list = [sp_engine.B[item] for item in selected_idx]
    return distance_list, path_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    'run dijkstra to identify shortest path')
    parser.add_argument('--file', '-f', type=str, help='data file path')
    args = parser.parse_args()
    source_vertex = 1

    start = time.time()
    selected_nodes = [7,37,59,82,99,115,133,165,188,197]
    # selected_nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    distance_list, path_list = run_sp_exp(args.file, selected_nodes,
    source_vertex=source_vertex)
    for i in range(len(distance_list)):
        print((f'The shortest distance from {source_vertex} to the ' 
            f'node #{selected_nodes[i]} is {distance_list[i]}'))
        print(f'This path is {path_list[i]}')
    print((f'The shortest distance of the selected node are:',
        f'{distance_list}'))
    end = time.time()
    time_elapsed = end - start
    print(f'the shortest path search experiment took \
    {timedelta(seconds=time_elapsed)}')

    