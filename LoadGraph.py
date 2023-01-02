import networkx as nx

class LoadGraph():
    
    def __init__(self):
        
        self.graph = nx.read_gexf('network1 7184 words.gexf')
        print(nx.info(self.graph))
        
        pass
    
    

if __name__ == '__main__':
    
    lg = LoadGraph()