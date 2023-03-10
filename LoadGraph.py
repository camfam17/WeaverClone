import networkx as nx
import random
from pyvis.network import Network
import webbrowser
import os


# add ability to choose start word and/or end word
# multithreading for path finding


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
        pass
    
    
    def get_new_game(self):
        
        ############ read in graph from file ############
        self.graph = nx.read_gexf('DataFiles/network file.gexf', node_type=int)
        print('Graph info:', nx.number_of_nodes(self.graph), 'nodes,', nx.number_of_edges(self.graph), 'edges')
        
        
        ############ create lists representing graph info ############
        self.node_data_view = self.graph.nodes(data=True)
        self.nodes = [None] * len(self.node_data_view) # list of dictionaries of labels i.e. [{'label': 'aahs'}, {}...]
        self.node_labels = [None] * len(self.node_data_view) # list of node labels with indices corresponding to node's number
        for n in self.node_data_view:
            self.nodes[n[0]] = n[1]
            self.node_labels[n[0]] = n[1]['label']
        
        
        ############ select a random start word ############
        self.start_node = self.choose_start_node()
        
        self.end_node = self.select_valid_end_node()
        
        shortest_paths = list(nx.all_shortest_paths(G=self.graph, source=self.start_node, target=self.end_node))
        print('shortest_paths', shortest_paths)
        shortest_paths_plus_1 = list(nx.all_simple_paths(G=self.graph, source=self.start_node, target=self.end_node, cutoff=len(shortest_paths[0])+1))
        # print('shortest_paths_plus_1', shortest_paths_plus_1)
        
        shortest_graphs = self.make_graph_from_list(shortest_paths)
        nx.write_gexf(shortest_graphs, 'DataFiles/shortest_graphs.gexf')
        
        shortest_graphs_plus_1 = self.make_graph_from_list(shortest_paths_plus_1)
        nx.write_gexf(shortest_graphs_plus_1, 'DataFiles/shortest_graphs_plus_1.gexf')
        
        print('Done')
        return self.start_node, self.end_node, shortest_paths
    
    
    # function to take shortest_graphs and shortest_graphs_plus_1 and colour all common nodes an different colour
    # TODO must remove redundancy between this and view_graph() function
    def colour_common_nodes(self):
        
        nxgraph1 = nx.read_gexf('DataFiles/shortest_graphs.gexf')
        nxgraph2 = nx.read_gexf('DataFiles/shortest_graphs_plus_1.gexf')
        
        nodeslist1 = nxgraph1.nodes()
        print('nodeslist1', nodeslist1)
        
        net2 = Network(heading='colour common nodes')
        net2.inherit_edge_colors(False)
        net2.from_nx(nxgraph2)
        
        for node in nodeslist1:
            net2.get_node(node)['color'] = '#A020F0'
        
        net2.get_node(str(self.start_node))['color'] = '#00FF00'
        net2.get_node(str(self.start_node))['shape'] = 'star'
        net2.get_node(str(self.end_node))['color'] = '#FF0000'
        net2.get_node(str(self.end_node))['shape'] = 'square'
        
        gen = net2.generate_html()
        output = open('DataFiles/colour_common.html', 'w')
        output.write(gen)
        output.close()
        self.display_graph_html('DataFiles/colour_common')
    
    
    def display_graph_html(self, filename):
        webbrowser.open_new_tab(os.getcwd() + '/' + filename + '.html')
    
    
    def create_pyvis_graph(self, filename='DataFiles/shortest_graphs.gexf'):
        
        # nx_graph = nx.read_gexf('DataFiles/shortest_graphs.gexf')
        nx_graph = nx.read_gexf(filename)
        
        net = Network(heading='Weaver Words')
        net.inherit_edge_colors(False)
        net.from_nx(nx_graph)
        
        net.get_node(str(self.start_node))['color'] = '#00FF00'
        net.get_node(str(self.start_node))['shape'] = 'star'
        net.get_node(str(self.end_node))['color'] = '#FF0000'
        net.get_node(str(self.end_node))['shape'] = 'square'
        
        start = net.get_node(str(self.start_node))
        end = net.get_node(str(self.end_node))
        # print('start:', start, 'end:', end)
        
        gen = net.generate_html()
        output = open(filename+'.html', 'w')
        output.write(gen)
        output.close()
        self.display_graph_html(filename)
    
    
    ############ find end word and path from start to end ############
    def select_valid_end_node(self):
        # USED FOR STRAT 2
        fail_count = -1
        while True:                      # NB: check that fail counter fixes infinite looping bug
            fail_count += 1
            end_node = random.randrange(0, len(self.graph.nodes)) # choose a random end node
            
            try:
                shortest_path = nx.shortest_path(G=self.graph, source=self.start_node, target=end_node) # ensure there is a path between start and end
            except nx.exception.NetworkXNoPath:
                continue
            
            print('fail count:', fail_count, 'end_word', self.nodes[end_node]['label'])
            if(fail_count > 100):
                self.start_node = self.choose_start_node()
                fail_count = -1
                continue
            
            ### TODO: should the 'end_node != self.start_node' be checked in the same line as 'end_node = random.randrange(0, len(self.graph.nodes))'?? (a few lines above)
            if end_node != self.start_node and len(shortest_path) < 11 and len(shortest_path) > 3: # ensure the length between start and end is 4-10 words long
                break
        print('end node:', end_node, ':', self.node_labels[end_node])
        print('shortest_path length:', len(shortest_path))
        
        return end_node
    
    
    def make_graph_from_list(self, path_list):
        
        shortest_graphs = nx.Graph()
        # TODO: write shortest_paths to a graph, with different path's edges in different colours?
        for i in range(len(path_list)):
            shortest_graphs.add_node(path_list[i][0], label=self.node_labels[path_list[i][0]])
            for j in range(1, len(path_list[i])):
                
                shortest_graphs.add_node(path_list[i][j], label=self.node_labels[path_list[i][j]])
                # shortest_graphs.add_node(j, label=self.node_labels[j])
                shortest_graphs.add_edge(path_list[i][j-1], path_list[i][j])
        
        return shortest_graphs
    
    
    def load_indices(self):
        
        file = open('DataFiles/fourletterwordlist.txt')
        four_letter_words = file.readlines()
        file.close()
        
        letter_index = {'a' : 0}
        for i in range(1, len(four_letter_words)):
            if four_letter_words[i][0] != four_letter_words[i-1][0]:
                letter_index[four_letter_words[i][0]] = i
        letter_index['{'] = len(four_letter_words)
        
        return letter_index
    
    
    def choose_start_node(self):
        while True:
            start_node = random.randrange(0, len(self.graph.nodes))
            if len(list(self.graph.neighbors(start_node))) > 0: # checking is the word has at least one neighbour - maybe check how many neighbours it has or how many levels of neighbours it has (how many neighbours does its neighbours have?)
                print('start node:', start_node, ':', self.node_labels[start_node])
                return start_node
    
    
    def differs_by_one(self, word1, word2):
        
        differ = 0
        for i in range(4):
            if not word1[i] == word2[i]:
                differ += 1
        
        return differ == 1
    


if __name__ == '__main__':
    
    lg = LoadGraph()
    lg.get_new_game()
    
    
    
    
    
    
    
    ############ create graph and save as file ############
    # shortest_graph = nx.Graph()
    # shortest_graph.add_node(self.start_node, label=self.node_labels[self.start_node])
    # for i in range(1, len(shortest_path)):
    #     shortest_graph.add_node(shortest_path[i], label=self.node_labels[shortest_path[i]])
    #     shortest_graph.add_edge(shortest_path[i-1], shortest_path[i])
    # nx.write_gexf(shortest_graph, 'DataFiles/shortest_graph.gexf')




    ##### USED FOR STRAT 1 #####
    # select minimum number of guesses to win game
    # if min_guesses == 0:
    #     min_guesses = random.randrange(4, 10)
    # min_guesses = 4
    # print('Min guesses', min_guesses)
    # self.steps_list = self.get_steps_list(n=min_guesses)


    # ### write func to take in list of node nums and return list of corresponding node names
    
    
    # # creates a list of lists neighbours[step][nodes]
    # # i.e. steps[1] is a list of all nodes 1 step away from source
    # # i.e. steps[2] is a list of all nodes 2 steps away from source
    # # not sure how useful this will be
    # def get_steps_list(self, n):
        
    #     steps = [list() for x in range(n)]
    #     steps[0].append(self.start_node)
    #     print(steps)
        
    #     steps_labels = [list() for x in range(n)]
    #     steps_labels[0].append(self.nodes[self.start_node]['label'])
        
    #     g = nx.Graph()
        
    #     visited = set()
    #     for i in range(1, 4):
    #         visited.update(steps[i-1])
    #         # print('i', i, ':', visited, end='')
            
    #         for prev_node in steps[i-1]:
    #             neighbours = list(self.graph.neighbors(prev_node))
    #             for num, neighbour in enumerate(neighbours):
    #                 if neighbour not in visited:
    #                     steps[i].append(neighbour)
    #                     steps_labels[i].append(self.nodes[neighbour]['label'])
                        
    #                     # NB constructing graph like this is flawed. Miss out many links due to no copies of nodes in steps
    #                     # see Graph 'h', recaculates differs_by_one for every node (n^2)
    #                     g.add_node(neighbour, label=self.nodes[neighbour]['label'])
    #                     g.add_node(prev_node, label=self.nodes[prev_node]['label'])
    #                     g.add_edge(neighbour, prev_node)
                
    #         # print()
        
    #     print(steps)
    #     print(steps_labels)
        
    #     nx.write_gexf(g, 'steps_graph.gexf')
        
    #     h = nx.Graph()
    #     count = 0
    #     for i in range(len(steps)):
    #         for j in range(len(steps[i])):
    #             h.add_node(count, label=steps_labels[i][j])
    #             count += 1
        
        
    #     for i in h.nodes(data=True):
    #         num1, lab1 = i[0], i[1]['label']
    #         # print(num1, lab1)
    #         for j in h.nodes(data=True):
    #             num2, lab2 = j[0], j[1]['label']
                
    #             if self.differs_by_one(lab1, lab2):
    #                 h.add_edge(num1, num2)
        
    #     nx.write_gexf(h, 'step graph recalc diff-by-one.gexf')
    
    
    # def bfsv2(self, n):
        
    #     # neighbours = [list() for x in range(n)]
    #     # neighbours[0].append(self.start_node)
        
    #     #bfs edge list n nodes deep frpm start node source
    #     bfs_edges = list(nx.bfs_edges(G=self.graph, source=self.start_node, depth_limit=n))
    #     print(bfs_edges)
        
        
    #     g = nx.Graph()
    #     for x in bfs_edges:
    #         print(x)
    #         node_num1 = x[0]
    #         node_label1 = self.nodes[node_num1]['label']
    #         node_num2 = x[1]
    #         node_label2 = self.nodes[node_num2]['label']
            
    #         g.add_node(node_num1, label=node_label1)
    #         g.add_node(node_num2, label=node_label2)
    #         g.add_edge(node_num1, node_num2)
        
    #     print(nx.info(g))
        
    #     last_word = (bfs_edges)[-1][1]
    #     print('last word', last_word, self.nodes[last_word])
        
    #     nx.write_gexf(g, 'cluster.gexf')
    
    
    # def bfsv1(self, n):
        
    #     neighbours = nx.bfs_edges(G=self.graph, source=self.start_node, depth_limit=n)
    #     print(neighbours)
        
    #     edges = []
    #     nodes = set()
    #     g = nx.Graph()
    #     for x in neighbours:
    #         # print(x)
    #         edges.append(x)
    #         node_num1 = x[0]
    #         node_label1 = self.nodes[node_num1]['label']
    #         node_num2 = x[1]
    #         node_label2 = self.nodes[node_num2]['label']
            
    #         if self.differs_by_one(node_label1, node_label2):
    #             g.add_node(node_num1, label=node_label1)
    #             g.add_node(node_num2, label=node_label2)
    #             g.add_edge(node_num1, node_num2)
                
            
    #         nodes.add((x[0], self.nodes[x[0]]['label']))
    #         nodes.add((x[1], self.nodes[x[1]]['label']))
        
    #     nx.write_gexf(g, 'g.gexf')
        
    #     print(edges)
    #     print(nodes)
    #     new_graph = nx.from_edgelist(edges, self.graph)
    #     nx.write_gexf(new_graph, 'smallgraph.gexf')
        
    #     # parse the list of edge-tuples into layers of neighbours
        
    #     return neighbours
    