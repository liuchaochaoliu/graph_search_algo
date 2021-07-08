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
                gr[int(items[0])-1] += [int(items[1])]
                r_gr[int(items[1])-1] += [int(items[0])]
        self.g = gr
        self.g_rev = r_gr
        
        # initialize list of finishing times
        self.f = [np.nan] * self.n
    
    def dfs_search(self, g, i):
        # set i as explored
        self.exp_list[i] = True
        # set i as leader
        self.leader_list[i] = self.s
        nbr_nodes = g[i]
        for nbr_node in nbr_nodes:
            new_node = nbr_node - 1
            # print(f'attempted new node is {new_node+1}')
            if not self.exp_list[new_node]:
                self.dfs_search(g, new_node)
        # update finishing time
        self.t = self.t + 1
        self.f[i] = self.t
        # print(f'The {i+1}th node was assigned finishing time of {self.t}')
                
    def dfs_loop(self, g, order='sequential'):
        assert order in ['sequential', 'finishing_time'], print('specify correct order')
        
        # initialization
        self.exp_list = [False] * self.n    
        self.leader_list = [np.nan] * self.n
        self.t = 0
        
        if order == 'sequential':         
            for i in reversed(range(self.n)):
                print(f'node_{i + 1} was processed')
                if not self.exp_list[i]:
                    self.s = i + 1
                    self.dfs_search(g, i)
        elif order == 'finishing_time':
            f_idx = np.argsort(-np.array(self.magical_order))
            for node_idx in f_idx:
                print(f'node_{node_idx + 1} was processed. its finishing value is  {self.f[node_idx]}')
                if not self.exp_list[node_idx]:
                    self.s = node_idx + 1
                    self.dfs_search(g, node_idx)
                
    def dfs_scc(self):
        # step 1: run dfs-loop on reversed graph
        self.dfs_loop(self.g_rev)
        self.magical_order = self.f.copy()
        # step 2: run dfs-loop on graph
        assert np.nan not in self.f, print('not every nodes has finishing time')
        self.dfs_loop(self.g, order='finishing_time')
        # step 3: group the nodes by SCC
        scc_df = pd.DataFrame(self.leader_list, columns=['leader'])
        return scc_df