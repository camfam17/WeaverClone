import networkx as nx
import random

class LoadGraph():
    
    def __init__(self, min_guesses=0):
        
        # read in graphh from file
        self.graph = nx.read_gexf('network1 7184 words.gexf', node_type=int)
        print('Graph info:', nx.info(self.graph))
        
        # select minimum number of guesses to win game
        if min_guesses == 0:
            min_guesses = random.randrange(4, 10)
        min_guesses = 4
        print('Min guesses', min_guesses)
        
        
        self.node_data_view = self.graph.nodes(data=True)
        self.nodes = [None] * len(self.node_data_view) # list of dictionaries of labels i.e. [{'label': 'aahs'}, {}...]
        for n in self.node_data_view:
            self.nodes[n[0]] = n[1]
        print('self.nodes', self.nodes)
        self.answer_path = []
        
        # select a random word
        self.start_node = random.randrange(0, len(self.graph.nodes))
        self.start_node = 1930
        print('start node:', self.start_node, ':', self.nodes[self.start_node])
        
        # self.neighbours = self.bfsv1(n=min_guesses)
        self.neighbours = self.bfsv2(n=min_guesses)
        # self.print_neighbours()
    
    
    def bfsv3(self, n):
        
        # implement own bfs to return desired structure (i.e. list of list of neighbours i.e. bfs_result[step][list of neighbours 'step' steps away])
        
        # NBNB!: g.adjacency --> Returns an iterator over (node, adjacency dict) tuples for all nodes.
        # use this for old approach of create your own datastructure
        
        
        
        pass
    
    
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
    
    
    def own_bfs(self):
        
        # implement own bfs to return desired structure (i.e. list of list of neighbours i.e. bfs_result[step][list of neighbours 'step' steps away])
        
        # NBNB!: g.adjacency --> Returns an iterator over (node, adjacency dict) tuples for all nodes.
        # use this for old approach of create your own datastructure
        pass
    
    def print_neighbours(self):
        print('printing neighbours...')
        print(self.neighbours)
    
    
    def differs_by_one(self, word1, word2):
        
        differ = 0
        for i in range(4):
            if not word1[i] == word2[i]:
                differ += 1
        
        return differ == 1


if __name__ == '__main__':
    
    lg = LoadGraph()
    
    # move all graph and dictionary editing into one file with multiple classes