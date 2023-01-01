import os
from pyvis.network import Network
import networkx as nx



def load_adjacency_list(file_name):
    file = open(file_name)
    adj_list = file.readlines()
    file.close()
    
    if len(adj_list[0]) < 3:
        adj_list.pop(0)
    
    return adj_list


def create_adjacency_dictionary(adj_list):
    
    graph_dict = {}
    for i, line in enumerate(adj_list):
        print('i:', i, end=' ')
        
        first_index = line.index(' ') + 1
        second_index = line.index(' ', first_index+1)
        
        num = line[:first_index]
        name = line[first_index:second_index]
        lst_str = line[second_index:]
        
        lst = lst_str.split(sep=', ')[:-1]
        lst = [int(x) for x in lst]
        
        print('num:', num, 'name:', name, 'lst_str:', lst_str, 'list:', lst)
        
        graph_dict[name] = lst
    
    return graph_dict


def add_nodes(graph_dict):
    for num, name in enumerate(graph_dict.keys()):
        net.add_node(n_id=int(num), label=name, color='pink', size=30, physics=True)


def add_edges(graph_dict):
    for num, adj_nodes in enumerate(graph_dict.values()):
        print(num)
        for adj_node in adj_nodes:
            # print('num', num, type(num), 'adj_node:', adj_node, type(adj_node))
            # net.add_edge(net.get_node(num), net.get_node(adj_node))
            try:
                net.add_edge(num, adj_node, physics=False)
            except:
                pass 
        




if __name__ == '__main__':
    
    adj_list = load_adjacency_list('AdjacencyList.txt')
    adj_list = adj_list[:300]
    
    adj_dict = create_adjacency_dictionary(adj_list)
    
    net = Network(width='1000px', height='1000px', bgcolor='#222222', font_color='white')
    net.barnes_hut()
    
    add_nodes(adj_dict)
    add_edges(adj_dict)
    
    graph_name = os.getcwd() + '\\graphs\\graph15.html'
    # net.show(graph_name)
    try:
        net.save_graph(graph_name)
    except:
        pass
    
    
    #TODO:
    # create adjacency matrix
    # create some sort of network storage data structure to save as file
    # investigate different network visualization modules