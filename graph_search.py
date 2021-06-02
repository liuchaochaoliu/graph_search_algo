import numpy as np
import pandas as pd

class dfs:
    '''
    This class is able to find the strongly connected components for a given graph g
    by applying Kosaraju's two-pass algorithm.
    '''
    
    def __init__(self, g):
        self.g = g
        g_heads = g.iloc[:, 1].unique().tolist()
        g_tails = g.iloc[:, 0].unique().tolist()
        self.vertices = np.unique(g_heads + g_tails).tolist()
        self.n = len(self.vertices)
        self.m = len(g)    
        self.f = [np.nan] * self.n

        g_rev = pd.concat([g.iloc[:, 1],  g.iloc[:, 0]], axis=1)
        g_rev.columns = g.columns
        self.g_rev = g_rev
    

    def dfs_search(self, g, i):
        '''
        this function does the dfs search and update finishing times recursively
        args:
        -g  : graph 
        -i  : initial node to launch dfs search
        '''

        # set i as explored
        self.exp_list[i] = True
        # set i as leader
        self.leader_list[i] = self.s
        arcs_out = [item for item in g.values if i == item[0]-1]
        # perform dfs search recursively
        for item in arcs_out:
            new_node = item[1] - 1
            if not self.exp_list[new_node]:
                self.dfs_search(g, new_node)
        # update finishing time
        self.t = self.t + 1
        self.f[i] = self.t
 

    def dfs_loop(self, g, order='sequential'):
        '''
        launch dfs search iteratively from unexplored nodes(leaders). It has two modes:
        1) sequantial mode: sequentially check if a node is explored based on their node index
        2) finish_time: check if a node is explored based on their finish time

        args:
        -g      : graph
        -order  : mode of running dfs_loop
        '''
        assert order in ['sequential', 'finishing_time'], print('specify correct order')
        
        # initialization
        self.exp_list = [False] * self.n    
        self.leader_list = [np.nan] * self.n
        self.t = 0
        counter = 0  
        
        if order == 'sequential':       
            for i in reversed(range(self.n)):
                counter = counter + 1
                print(f'node_{i} was processed. {counter} of {self.n} nodes have been processed')
                if not self.exp_list[i]:
                    self.s = i + 1
                    self.dfs_search(g, i)
        elif order == 'finishing_time':
            f_idx = np.argsort(-np.array(self.magical_order))
            for node_idx in f_idx:
                counter = counter + 1
                print(f'node_{node_idx} was processed. {counter} of {self.n} nodes have been processed')
                if not self.exp_list[node_idx]:
                    self.s = node_idx + 1
                    self.dfs_search(g, node_idx)
    

    def dfs_scc(self):
        '''
        this function carries out the Kosaraju's two pass algorithm and return the groups
        of nodes based on their leader nodes

        '''

        # step 1: run dfs-loop on reversed graph
        self.dfs_loop(self.g_rev)
        self.magical_order = self.f.copy()
        print(f'1st pass of dfs-loop on reversed graph was successfully completed')

        # step 2: run dfs-loop on graph
        assert np.nan not in self.f, print('not every nodes has finishing time')
        self.dfs_loop(self.g, order='finishing_time')
        print(f'2nd pass of dfs-loop on the actual graph was successfully completed')

        # step 3: group the nodes by SCC
        scc_df = pd.DataFrame(self.leader_list, columns=['leader'])

        return scc_df