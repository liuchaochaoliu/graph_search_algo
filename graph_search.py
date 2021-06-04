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

        print(self.g_rev)
    

    def dfs_search(self, g):
        '''
        this function does the dfs search and update finishing times recursively
        args:
        -g  : graph 
        '''
        while self.stack:
                    
            print('stack initial reation')
            print([item+1 for item in self.stack])

            i = self.stack[0] # first element in stack
            # set i as explored
            self.exp_list[i] = True
            # set i as leader
            self.leader_list[i] = self.s


            # build stacks (firt in first out)
            done = True
            nbr_nodes = g[i]
            for nbr_node in nbr_nodes:
                new_node = nbr_node - 1
                if not self.exp_list[new_node]:
                    self.stack = [new_node] + self.stack
                    self.exp_list[new_node] = True
                    done = False
                    print('stack creation')
                    print([item+1 for item in self.stack])

            # update finishing time
            if done:
                self.t = self.t + 1
                self.f[i] = self.t
                self.order = [i] + self.order
                print('stack elimination:')
                print([item+1 for item in self.stack])
                print(f't = {self.t}')
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
        self.exp_list = [False] * self.n    
        self.leader_list = [np.nan] * self.n
        self.stack = []
        self.t = 0
        self.order = []
        counter = 0  
        
        if mode == 'sequential':       
            for i in reversed(range(self.n)):
                counter = counter + 1
                print(f'node_{i+1} was processed. {counter} of {self.n} nodes have been processed')
                if not self.exp_list[i]:
                    self.s = i + 1
                    self.stack = [i]
                    self.dfs_search(g)

        elif mode == 'finishing_time':
            for node_idx in self.magical_order:
                counter = counter + 1
                print(f'node_{node_idx+1} was processed. its finishing value is  {self.magical_order[node_idx]}.\
                    {counter} of {self.n} nodes have been processed')
                if not self.exp_list[node_idx]:
                    self.s = node_idx + 1
                    self.stack = [node_idx]
                    self.dfs_search(g)
    

    def dfs_scc(self):
        '''
        this function carries out the Kosaraju's two pass algorithm and return the groups
        of nodes based on their leader nodes

        '''

        # step 1: run dfs-loop on reversed graph
        self.dfs_loop(self.g_rev)
        self.magical_order = self.order.copy()
        print(f'1st pass of dfs-loop on reversed graph was successfully completed')
        print(f'finishing values are {self.f}')
        print(f'magical orders are {[item+1 for item in self.magical_order]}')

        # step 2: run dfs-loop on graph
        assert np.nan not in self.f, print('not every nodes has finishing time')
        self.dfs_loop(self.g, mode='finishing_time')
        print(f'2nd pass of dfs-loop on the actual graph was successfully completed')

        # step 3: group the nodes by SCC
        scc_df = pd.DataFrame(self.leader_list, columns=['leader'])

        return scc_df