import os
# from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
# from dash import Dash, html
# import dash_cytoscape as cyto



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
        # print('i:', i, end=' ')
        
        first_index = line.index(' ') + 1
        second_index = line.index(' ', first_index+1)
        
        num = line[:first_index]
        name = line[first_index:second_index]
        lst_str = line[second_index:]
        
        lst = lst_str.split(sep=', ')[:-1]
        lst = [int(x) for x in lst]
        
        # print('num:', num, 'name:', name, 'lst_str:', lst_str, 'list:', lst)
        
        graph_dict[name] = lst
    
    return graph_dict


# def add_nodes_pyvis(graph_dict):
#     for num, name in enumerate(graph_dict.keys()):
#         net.add_node(n_id=int(num), label=name, color='pink', size=30, physics=True)


# def add_edges_pyvis(graph_dict):
#     for num, adj_nodes in enumerate(graph_dict.values()):
#         print(num)
#         for adj_node in adj_nodes:
#             # print('num', num, type(num), 'adj_node:', adj_node, type(adj_node))
#             # net.add_edge(net.get_node(num), net.get_node(adj_node))
#             try:
#                 net.add_edge(num, adj_node, physics=False)
#             except:
#                 pass 
        


def create_nx_graph(adj_dict):
    
    for num, item in enumerate(adj_dict.items()):
        print(num)
        nxnet.add_node(num, label=item[0])
        
        for adj_node in item[1]:
            if adj_node < size:
                nxnet.add_edge(num, adj_node)
        
    # net.add_nodes_from(adj_dict.keys())
    print(nxnet)


# def add_nk_labels(adj_dict):
    
#     for num, label in enumerate(adj_dict.keys()):
#         labels[num] = label


# def add_nk_edges(adj_dict):
    
#     for num, value in enumerate(adj_dict.values()):
#         for adj_node in value:
            
#             if adj_node < size:
#                 nknet.addEdge(num, adj_node)
    
#     pass


if __name__ == '__main__':
    
    adj_list = load_adjacency_list('AdjacencyList.txt')
    
    size = len(adj_list)
    # size = 300
    adj_list = adj_list[:size]
    
    adj_dict = create_adjacency_dictionary(adj_list)
    
    graph_name = os.getcwd() + '\\graphs\\graph15.html'
    
    
    nxnet = nx.Graph()
    create_nx_graph(adj_dict)
    labels = nx.get_node_attributes(nxnet, 'label')
    plt.figure(figsize=(9, 9))
    # nx.draw(nxnet, labels=labels)
    nx.draw_random(nxnet, labels=labels)
    # nx.draw_shell(nxnet, labels=labels)
    
    
    nx.write_gexf(nxnet, 'output1.gexf')
    
    
    plt.show()
    
    
    
    #TODO:
    # create adjacency matrix
    # create some sort of network storage data structure to save as file
    # investigate different network visualization modules



# net = Network(width='1000px', height='1000px', bgcolor='#222222', font_color='white')
# net.barnes_hut()
# add_nodes_pyvis(adj_dict)
# add_edges_pyvis(adj_dict)
# try:
#     net.save_graph(graph_name)
# except:
#     pass


# pyvis_net = Network()
# pyvis_net.from_nx(nxnet)
# pyvis_net.show('pyvis graph1.html')

# nknet = nk.Graph(size, directed=False, weighted=False)
# labels = nknet.attachNodeAttribute('label', str)
# add_nk_labels(adj_dict)
# add_nk_edges(adj_dict)

# nknet = nk.nxadapter.nx2nk(nxnet)

# print(nk.overview(nknet))
# nk.viztasks.drawGraph(nknet, labels=labels)
# plt.show()