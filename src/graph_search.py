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


class shortest_path:
    '''
    This class identifies the shortest paths from a source vertex to all the other vertices
    in an undirected graph g, via the Dijkstra's algorithm
    '''
    def __init__(self, filename):
        # import txt file
        self.n = 0
        file = open(filename, 'r')
        data = file.readlines()

        # find the total number of vertices
        for line in data:
            if line != '\n':
                self.n += 1
        print(f'there are totally {self.n} vertices in this graph')

        # create graph file
        self.gr = [[] for i in range(self.n)]
        self.vertices = set()
        for line in data:
            if line != '\n':
                vertex = int(line.split()[0])
                self.vertices.add(vertex - 1)
                arcs = []
                for arc_string in line.split()[1:]:
                    [outer_node, length] = arc_string.split(',')
                    arc = tuple([int(outer_node)-1, int(length)])
                    arcs.append(arc)
            self.gr[vertex-1] = arcs

    def sp_search(self, source_vertex=1):
        # step 1: initialization
        source_idx = source_vertex - 1
        X = [source_idx]
        A = [None for i in range(self.n)]
        B = [[] for i in range(self.n)]
        A[source_idx] = 0
        B[source_idx]= []

        # step 2: grow frontier
        while set(X) != self.vertices:
            # 2.1 identify the edges across frontier and update outer nodes' 
            # greedy values
            new_edges = []
            for inner_idx, arcs in enumerate(self.gr):
                if inner_idx not in X:
                    continue
                for arc in arcs:
                    outer_idx = arc[0]
                    arc_length = arc[1]
                    if outer_idx in X:
                        continue
                    A_new_node = A[inner_idx] + arc_length
                    new_edges.append((inner_idx, outer_idx, A_new_node))

            # 2.2 identify the shortest newly added path
            A_new_edges = [item[-1] for item in new_edges]
            selected_new_edge = new_edges[np.argmin(A_new_edges)]
            w = selected_new_edge[1]

            assert w not in X, print('The selected outer not was examined already')
            assert A[selected_new_edge[0]] is not None, print('The tail of selected \
            node was not processed') 
            X.append(w)
            A[w] = selected_new_edge[-1]
            B[w] = B[selected_new_edge[0]] + [w]

        # step 3: treat those unreachable nodes 
        for i, value in enumerate(A):
            if value is None:
                A[i] = 1000000
                B[i] = None
        self.A = A
        
        # step 4: recover idx to node for self.B
        for i, path in enumerate(B):
            if path is not None:
                updated_path = [item+1 for item in path]
            B[i] = updated_path
        self.B = B