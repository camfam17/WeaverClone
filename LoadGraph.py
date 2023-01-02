import networkx as nx
import random

class LoadGraph():
    
    def __init__(self, min_guesses=0):
        
        self.graph = nx.read_gexf('network1 7184 words.gexf', node_type=int)
        print('Graph info:', nx.info(self.graph))
        
        if min_guesses == 0:
            min_guesses = random.randrange(4, 10)
        min_guesses = 4
        print('Min guesses', min_guesses)
        
        self.node_data_view = self.graph.nodes(data=True)
        
        self.nodes = [None] * len(self.node_data_view)
        for n in self.node_data_view:
            self.nodes[n[0]] = n[1]
        
        self.answer_path = []
        
        # self.start_node = self.select_start_word()
        self.start_node = random.randrange(0, len(self.graph.nodes))
        print('start node:', self.start_node)
        
        self.neighbours = self.get_n_steps_neighbours(n=min_guesses)
        self.print_neighbours()
    
    
    def select_start_word(self):
        
        rand_num = random.randrange(0, len(self.graph.nodes))
        
        rand_word = self.nodes[rand_num]['label']
        
        print(rand_num, rand_word)
        
        # neighbors = self.graph.neighbors(rand_num)
        # for n in neighbors:
        #     print(n, self.nodes[n]['label'])
        
        return rand_num
    
    
    def get_n_steps_neighbours(self, n):
        
        # neighbours[step] = list of neighbours 'step' steps away
        
        neighbours = [list() for i in range(n)]
        print('neighbours init', neighbours)
        
        neighbours[0].append(self.start_node) # append start node at 0 steps away
        print('neighbours init2', neighbours)
        
        for i in range(1, 3):
            
            prev_list = neighbours[i-1]
            next_list = []
            for node in prev_list:
                print(type(node))
                neis = self.graph.neighbors(node)
                neis = list(neis)
                next_list.append(neis)
            neighbours[i] = next_list
        
        return neighbours
    
    
    def print_neighbours(self):
        print('printing neighbours...')
        print(self.neighbours)

if __name__ == '__main__':
    
    lg = LoadGraph()