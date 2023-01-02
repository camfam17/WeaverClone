import networkx as nx
import random

class LoadGraph():
    
    def __init__(self, min_guesses=0):
        
        self.graph = nx.read_gexf('network1 7184 words.gexf', node_type=int)
        print(nx.info(self.graph))
        
        if min_guesses == 0:
            self.min_guesses = random.randrange(4, 10)
        
        
        self.node_data_view = self.graph.nodes(data=True)
        
        self.nodes = [None] * len(self.node_data_view)
        for n in self.node_data_view:
            # print(n)
            self.nodes[n[0]] = n[1]
        
        # print(self.nodes)
        # print('self.nodes', type(self.nodes))
        
        # self.nodes[node number][attribute name]
        
        self.answer_path = []
        
        self.select_start_word()
    
    
    def select_start_word(self):
        
        rand_num = random.randrange(0, len(self.graph.nodes))
        
        rand_word = self.nodes[rand_num]['label']
        
        print(rand_num, rand_word)
        
        neighbors = self.graph.neighbors(rand_num)
        for n in neighbors:
            print(n, self.nodes[n]['label'])
        
    

if __name__ == '__main__':
    
    lg = LoadGraph()