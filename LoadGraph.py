import networkx as nx
import random

class LoadGraph():
    
    # STRAT 1
    # 1) load in graph file
    # 2) choose a random start word
    # 3) choose a minimum number of guess to get there
    # 4) create steps list that is min_guess long
    # 5) select random end word from final step
    # 6) find shortest path/s between start word and end word 
    # 7) find alternate, longer paths that the user may have taken
    
    # OR
    
    # STRAT 2
    # 2) choose a random start word
    # 3) choose a random end word
    # 4) find shortest path/s between start word and end word (and ensure its a reasonable number of guesses away i.e. 4-10 guesses)
    # 5) find alternate, longer paths that the user may have taken.
    
    
    def __init__(self):
        #fjd
        # self.get_new_game()
        pass
        
    
    def get_new_game(self):
        
        # read in graph from file
        self.graph = nx.read_gexf('network3 2294 words.gexf', node_type=int)
        print('Graph info:', nx.number_of_nodes(self.graph), 'nodes,', nx.number_of_edges(self.graph), 'edges')
        
        
        self.node_data_view = self.graph.nodes(data=True)
        self.nodes = [None] * len(self.node_data_view) # list of dictionaries of labels i.e. [{'label': 'aahs'}, {}...]
        self.node_labels = [None] * len(self.node_data_view) # list of node labels with indices corresponding to node's number
        for n in self.node_data_view:
            self.nodes[n[0]] = n[1]
            self.node_labels[n[0]] = n[1]['label']
        
        # select a random start word
        while True:
            self.start_node = random.randrange(0, len(self.graph.nodes))
            
            if len(list(self.graph.neighbors(self.start_node))) > 0:
                break
            
        print('start node:', self.start_node, ':', self.node_labels[self.start_node])
        
        
        ##### USED FOR STRAT 1 #####
        # select minimum number of guesses to win game
        # if min_guesses == 0:
        #     min_guesses = random.randrange(4, 10)
        # min_guesses = 4
        # print('Min guesses', min_guesses)
        # self.steps_list = self.get_steps_list(n=min_guesses)
        
        
        # USED FOR STRAT 2
        # NB: BUG - this loop just spins if the start word as no neighbours. 
        # first check that the start word has neighbours 
        # and maybe have a failure counter and if the counter goes above a certain threshold then a new start word is chosen
        while True:
            self.end_node = random.randrange(0, len(self.graph.nodes))
            
            try:
                shortest_path = nx.shortest_path(G=self.graph, source=self.start_node, target=self.end_node)
            except nx.exception.NetworkXNoPath:
                continue
            
            if self.end_node != self.start_node and len(shortest_path) < 11 and len(shortest_path) > 3:
                break
        print('end node:', self.end_node, ':', self.node_labels[self.end_node])
        
        shortest_paths = list(nx.all_shortest_paths(G=self.graph, source=self.start_node, target=self.end_node))
        # all_paths = nx.all_simple_paths(G=self.graph, source=self.start_node, target=self.end_node, cutoff=6)
        
        print('shortest_path', shortest_path)
        print('shortest_paths', shortest_paths)
        # print('all_paths:', all_paths)
        
        shortest_graph = nx.Graph()
        shortest_graph.add_node(self.start_node, label=self.node_labels[self.start_node])
        for i in range(1, len(shortest_path)):
            shortest_graph.add_node(shortest_path[i], label=self.node_labels[shortest_path[i]])
            shortest_graph.add_edge(shortest_path[i-1], shortest_path[i])
        nx.write_gexf(shortest_graph, 'shortest_graph.gexf')
        
        shortest_graphs = nx.Graph()
        # TODO: write shortest_paths to a graph, with different path's edges in different colours?
        for i in range(len(shortest_paths)):
            shortest_graphs.add_node(shortest_paths[i][0], label=self.node_labels[shortest_paths[i][0]])
            for j in range(1, len(shortest_paths[i])):
                
                shortest_graphs.add_node(shortest_paths[i][j], label=self.node_labels[shortest_paths[i][j]])
                # shortest_graphs.add_node(j, label=self.node_labels[j])
                shortest_graphs.add_edge(shortest_paths[i][j-1], shortest_paths[i][j])
        nx.write_gexf(shortest_graphs, 'shortest_graphs.gexf')
        
        print('Done')
        return self.start_node, self.end_node, shortest_path, shortest_paths
    
    ### write func to take in list of node nums and return list of corresponding node names
    
    
    # creates a list of lists neighbours[step][nodes]
    # i.e. steps[1] is a list of all nodes 1 step away from source
    # i.e. steps[2] is a list of all nodes 2 steps away from source
    # not sure how useful this will be
    def get_steps_list(self, n):
        
        steps = [list() for x in range(n)]
        steps[0].append(self.start_node)
        print(steps)
        
        steps_labels = [list() for x in range(n)]
        steps_labels[0].append(self.nodes[self.start_node]['label'])
        
        g = nx.Graph()
        
        visited = set()
        for i in range(1, 4):
            visited.update(steps[i-1])
            # print('i', i, ':', visited, end='')
            
            for prev_node in steps[i-1]:
                neighbours = list(self.graph.neighbors(prev_node))
                for num, neighbour in enumerate(neighbours):
                    if neighbour not in visited:
                        steps[i].append(neighbour)
                        steps_labels[i].append(self.nodes[neighbour]['label'])
                        
                        # NB constructing graph like this is flawed. Miss out many links due to no copies of nodes in steps
                        # see Graph 'h', recaculates differs_by_one for every node (n^2)
                        g.add_node(neighbour, label=self.nodes[neighbour]['label'])
                        g.add_node(prev_node, label=self.nodes[prev_node]['label'])
                        g.add_edge(neighbour, prev_node)
                
            # print()
        
        print(steps)
        print(steps_labels)
        
        nx.write_gexf(g, 'steps_graph.gexf')
        
        h = nx.Graph()
        count = 0
        for i in range(len(steps)):
            for j in range(len(steps[i])):
                h.add_node(count, label=steps_labels[i][j])
                count += 1
        
        
        for i in h.nodes(data=True):
            num1, lab1 = i[0], i[1]['label']
            # print(num1, lab1)
            for j in h.nodes(data=True):
                num2, lab2 = j[0], j[1]['label']
                
                if self.differs_by_one(lab1, lab2):
                    h.add_edge(num1, num2)
        
        nx.write_gexf(h, 'step graph recalc diff-by-one.gexf')
    
    
    def bfsv2(self, n):
        
        # neighbours = [list() for x in range(n)]
        # neighbours[0].append(self.start_node)
        
        #bfs edge list n nodes deep frpm start node source
        bfs_edges = list(nx.bfs_edges(G=self.graph, source=self.start_node, depth_limit=n))
        print(bfs_edges)
        
        
        g = nx.Graph()
        for x in bfs_edges:
            print(x)
            node_num1 = x[0]
            node_label1 = self.nodes[node_num1]['label']
            node_num2 = x[1]
            node_label2 = self.nodes[node_num2]['label']
            
            g.add_node(node_num1, label=node_label1)
            g.add_node(node_num2, label=node_label2)
            g.add_edge(node_num1, node_num2)
        
        print(nx.info(g))
        
        last_word = (bfs_edges)[-1][1]
        print('last word', last_word, self.nodes[last_word])
        
        nx.write_gexf(g, 'cluster.gexf')
    
    
    def bfsv1(self, n):
        
        neighbours = nx.bfs_edges(G=self.graph, source=self.start_node, depth_limit=n)
        print(neighbours)
        
        edges = []
        nodes = set()
        g = nx.Graph()
        for x in neighbours:
            # print(x)
            edges.append(x)
            node_num1 = x[0]
            node_label1 = self.nodes[node_num1]['label']
            node_num2 = x[1]
            node_label2 = self.nodes[node_num2]['label']
            
            if self.differs_by_one(node_label1, node_label2):
                g.add_node(node_num1, label=node_label1)
                g.add_node(node_num2, label=node_label2)
                g.add_edge(node_num1, node_num2)
                
            
            nodes.add((x[0], self.nodes[x[0]]['label']))
            nodes.add((x[1], self.nodes[x[1]]['label']))
        
        nx.write_gexf(g, 'g.gexf')
        
        print(edges)
        print(nodes)
        new_graph = nx.from_edgelist(edges, self.graph)
        nx.write_gexf(new_graph, 'smallgraph.gexf')
        
        # parse the list of edge-tuples into layers of neighbours
        
        return neighbours
    
    def differs_by_one(self, word1, word2):
        
        differ = 0
        for i in range(4):
            if not word1[i] == word2[i]:
                differ += 1
        
        return differ == 1


if __name__ == '__main__':
    
    lg = LoadGraph()
    lg.get_new_game()
    
    # move all graph and dictionary editing into one file with multiple classes