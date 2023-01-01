from pyvis.network import Network
import networkx as nx

net = Network(width='1000px', height='1000px', bgcolor='#222222', font_color='white')
net.barnes_hut()

graph_dict = {}

adj_list = open('AdjacencyList.txt').readlines()
# adj_list = ['2 aani 288, 353, 515, 1380, 4039, 4823, 5295, ']

if len(adj_list[0]) < 3:
    adj_list.pop(0)

adj_list = adj_list[:1000]

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
    
    net.add_node(n_id=int(num), label=name, color='blue', size=30, physics=True)


# for node in net.get_nodes():
#     print('node:', node)


for num, adj_nodes in enumerate(graph_dict.values()):
    print(num)
    for adj_node in adj_nodes:
        # print('num', num, type(num), 'adj_node:', adj_node, type(adj_node))
        # net.add_edge(net.get_node(num), net.get_node(adj_node))
        try:
            net.add_edge(num, adj_node, physics=False)
        except:
            pass    
    

net.show('graphs/graph7.html')

print('graph_dict:', graph_dict)