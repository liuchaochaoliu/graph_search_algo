import numpy as np
import pandas as pd

class dfs:
    '''
    This class is able to find the strongly connected components for a given graph g
    by applying Kosaraju's two-pass algorithm.
    '''
    
    def __init__(self, filename):
        # import txt file
        g_df = pd.read_csv(filename, sep=' ', header=None)
        if len(g_df.columns) > 2:
            g_df = g_df.drop(g_df.columns[2:], axis=1)
        g_heads = g_df.iloc[:, 1].unique().tolist()
        g_tails = g_df.iloc[:, 0].unique().tolist()
        self.vertices = np.unique(g_heads + g_tails).tolist()
        self.n = len(self.vertices)
        self.m = len(g_df) 
        print(f'there are {self.n} nodes and {self.m} edges in the loaded file')
        
        # prepare graph and reversed graph in the right formats
        gr =[[] for i in range(self.n)]
        r_gr = [[] for i in range(self.n)]
        file = open(filename, 'r')
        data = file.readlines()
        for line in data:
            if line != '\n':
                items = line.split()
                gr[int(items[0])-1] += [int(items[1])-1]
                r_gr[int(items[1])-1] += [int(items[0])-1]
        self.g = gr
        self.g_rev = r_gr
    

    def dfs_search(self, g, leader_node):
        '''
        this function does the dfs search and update finishing times recursively
        args:
        -g              : graph 
        -leader_node    : starting node for a dfs search
        '''
        self.stack = [leader_node]
        while self.stack:

            print(f'stack head is {self.stack[0]}. stack length is {len(self.stack)}. leader_node is {leader_node}')

            i = self.stack[0] # first element in stack
            del self.stack[0]

            if self.exp_list[i] != 'black':
                # add i to the stack
                self.stack = [i] + self.stack
                # set i as leader
                self.leader_list[i] = leader_node + 1

                # handle undiscovered initial node
                if self.exp_list[i] == 'white':
                    self.exp_list[i] = 'grey'
                    self.t = self.t + 1

                # handle undiscovered neighbouring nodes to initial node
                all_adj_discovered = True
                nbr_nodes = g[i]
                for nbr_node in nbr_nodes:
                    # new_node = nbr_node - 1
                    if self.exp_list[nbr_node] == 'white':
                        self.stack = [nbr_node] + self.stack
                        all_adj_discovered = False

                # handle the case whereby all neighboring nodes were discovered
                if all_adj_discovered:
                    self.exp_list[i] = 'black'
                    self.t = self.t + 1
                    self.f[i] = self.t
                    del self.stack[0]
 

    def dfs_loop(self, g, mode='sequential'):
        '''
        launch dfs search iteratively from unexplored nodes(leaders). It has two modes:
        1) sequantial mode: sequentially check if a node is explored based on their node index
        2) finish_time: check if a node is explored based on their finish time

        args:
        -g      : graph
        -mode  : mode of running dfs_loop
        '''
        assert mode in ['sequential', 'finishing_time'], print('specify correct mode')
        
        # initialization
        self.exp_list = ['white'] * self.n    
        self.leader_list = [np.nan] * self.n
        self.stack = []
        self.t = 0
        self.order = []
        self.f = [np.nan] * self.n
        counter = 0
        
        if mode == 'sequential':       
            for i in reversed(range(self.n)):
                counter = counter + 1
                print(f'{counter} nodes have been processedin the first pass')
                if self.exp_list[i] == 'white': 
                    self.dfs_search(g, i)   

        elif mode == 'finishing_time':
            self.magical_order = np.argsort(-np.array(self.finishing_time))
            for node_idx in self.magical_order:
                counter = counter + 1
                print(f'{counter} nodes have been processedin the first pass')
                if self.exp_list[node_idx] == 'white':
                    self.dfs_search(g, node_idx)
    

    def dfs_scc(self):
        '''
        this function carries out the Kosaraju's two pass algorithm and return the groups
        of nodes based on their leader nodes

        '''

        # step 1: run dfs-loop on reversed graph
        self.dfs_loop(self.g_rev)
        self.finishing_time = self.f.copy()
        print(f'1st pass of dfs-loop on reversed graph was successfully completed')
        print(f'the finishing times are {self.finishing_time}')

        # step 2: run dfs-loop on graph
        assert np.nan not in self.finishing_time, print('not every nodes has finishing time')
        self.dfs_loop(self.g, mode='finishing_time')
        print(f'the magical order is {self.magical_order}')
        print(f'2nd pass of dfs-loop on the actual graph was successfully completed')

        # step 3: group the nodes by SCC
        scc_df = pd.DataFrame(self.leader_list, columns=['leader'])

        return scc_df