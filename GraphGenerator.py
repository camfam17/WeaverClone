import networkx as nx
import matplotlib.pyplot as plt

nxnet = nx.Graph()

# take a dictionary of words and create a textfile of all the words contianing four letters
def edit_dictionary(dictionary_name, four_letter_dictionary_name):
    dict_file = open(dictionary_name)
    lines = dict_file.readlines()
    dict_file.close()
    
    new_dict = ''
    for word in lines:
        if(len(word) == 5 and word[-1] == '\n'):
            new_dict += word
    
    new_dict_file = open(four_letter_dictionary_name, 'w')
    new_dict_file.write(new_dict)
    new_dict_file.close()
    print('Four letter words saved to', four_letter_dictionary_name)


# take a list of four letter words and create a graph adjacency list where the nodes are the words and nodes are adjacent if they have one positional letter different
def create_adjacency_list(four_letter_dictionary_name, adjacency_list_name):
    four_letter_words = open(four_letter_dictionary_name).readlines()
    
    string = ''
    
    # n^2 for n = 7186
    for i, word1 in enumerate(four_letter_words):
        string += '\n' + str(i) + ' ' + word1[:-1] + ' '
        for j, word2 in enumerate(four_letter_words):
            
            if differs_by_one(word1, word2):
                string += str(j) + ', '
            
    
    print('stings', string)
    
    output_file = open(adjacency_list_name, 'w')
    output_file.write(string)


# create a graph file of type .gexf
def create_graph(adjacency_list_name, graph_file_name):
    adj_list = load_adjacency_list(adjacency_list_name)
    
    size = len(adj_list)
    # size = 300
    adj_list = adj_list[:size]
    
    adj_dict = create_adjacency_dictionary(adj_list)
    print(adj_dict)
    
    print('size:', size, 'len(adj_list):', len(adj_list), 'len(adj_dict):', len(adj_dict))
    
    create_nx_graph(adj_dict)
    
    nx.write_gexf(nxnet, graph_file_name)


# read in adjacency list file
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


def create_nx_graph(adj_dict):
    
    for num, item in enumerate(adj_dict.items()):
        nxnet.add_node(num, label=item[0])
        
        for adj_node in item[1]:
            if adj_node < len(adj_dict):
                nxnet.add_edge(num, adj_node)
        
    # net.add_nodes_from(adj_dict.keys())
    print(nxnet)


def differs_by_one(word1, word2):
    
    differ = 0
    for i in range(4):
        if not word1[i] == word2[i]:
            differ += 1
    
    return differ == 1


if __name__ == '__main__':
    
    dictionary_name = 'DataFiles/wordlist.txt'
    four_letter_dictionary_name = 'DataFiles/fourletterwordlist.txt'
    adjacency_list_name = 'DataFiles/AdjacencyList.txt'
    graph_file_name = 'DataFiles/network file.gexf'
    
    
    edit_dictionary(dictionary_name, four_letter_dictionary_name)
    create_adjacency_list(four_letter_dictionary_name, adjacency_list_name)
    create_graph(adjacency_list_name, graph_file_name)
    
    print('Done')