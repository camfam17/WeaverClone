from customtkinter import *
from LoadGraph import LoadGraph

# reset button - DONE NEEDS TESTING
# 'view graph' button
# refactor if statements inside key_press function

letter_tile_length = 75
word_frame_width = 4*75 + 8*10 # = 380
word_frame_height = letter_tile_length + 20 # = 95

inbetween_frames = 4 # number of word frames in between start_word_frame and end_word_frame before needing to scroll

words = []

class WordFrame(CTkFrame):
    
    def __init__(self, container, **kwargs):
        super().__init__(container)
        
        try:
            self.static_word = kwargs['static_word']
        except KeyError:
            self.static_word = '    '
        
        font1 = CTkFont(family='Arial', size=35, weight='bold')
        
        self.tiles = []
        for i in range(4):
            tile = CTkLabel(master=self, text=self.static_word[i], font=font1, bg_color='grey', width=letter_tile_length, height=letter_tile_length)
            self.tiles.append(tile)
            self.tiles[-1].grid(row=1, column=i*50, padx=10, pady=10)
    
    
    def update(self):
        for i in range(4):
            if i < len(words[-1]):
                self.tiles[i].configure(text=words[-1][i])
            else:
                self.tiles[i].configure(text=' ')
        self.static_word = words[-1]
    
    
    def colour(self):
        for i in range(4):
            if self.static_word[i] == end_word[i]:
                self.tiles[i].configure(bg_color='green')
    
    
    def uncolour(self):
        for tile in self.tiles:
            tile.configure(bg_color='grey')


class Main(CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("WeaverClone")
        self.resizable(False, False)
        self.bind('<Key>', self.key_press)
        self.bind('<MouseWheel>', self.mouse_wheel)
        
        self.is_game_over = False
        
        self.start_word_frame = WordFrame(self, static_word=start_word)
        self.start_word_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.start_word_frame.colour()
        self.end_word_frame = WordFrame(self, static_word=end_word)
        self.end_word_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        self.mainframe = CTkFrame(master=self) # , border_color='red', border_width=5
        self.mainframe.grid(row=1, column=1)
        
        self.scrollcanvas = CTkCanvas(master=self.mainframe, width=word_frame_width, height=word_frame_height) #, highlightbackground='green', highlightthickness=5
        self.scrollcanvas.grid(row=2, column=1)
        
        self.scrollbar = CTkScrollbar(master=self.mainframe, hover=False, orientation='vertical', width=18, height=word_frame_height) #, fg_color='pink'
        self.scrollbar.grid(row=0, column=100, rowspan=100)
        
        self.scrollwindow = CTkFrame(master=self.scrollcanvas, width=word_frame_width+20) # , border_color='blue', border_width=5
        self.scrollcanvas.create_window((0, 0), window=self.scrollwindow, anchor='nw')
        
        self.message_label = CTkLabel(master=self, text='', width=word_frame_width, height=50, bg_color='#c5bebe')
        self.message_label.grid(row=3, column=1)
        
        self.new_game_button = CTkButton(master=self, text='New Game', command=self.new_game)
        self.new_game_button.grid(row=4, column=1, pady=5)
        
        self.graph_button = CTkButton(master=self, text='View Graph', command=self.view_graph)
        self.graph_button.grid(row=5, column=1, pady=5)
        
        self.word_frames = []
        self.create_new_word_frame()
    
    
    def view_graph(self):
        g.view_graph()
    
    
    def new_game(self):
        
        print('restart')
        global words, start_word, end_word
        words = []
        
        start_node, end_node, shortest_paths = g.get_new_game()
        start_word = four_letter_words[start_node][:-1]
        end_word = four_letter_words[end_node][:-1]
        
        self.start_word_frame = WordFrame(self, static_word=start_word)
        self.start_word_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.start_word_frame.colour()
        self.end_word_frame = WordFrame(self, static_word=end_word)
        self.end_word_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        for word_frame in self.word_frames:
            word_frame.destroy()
        self.word_frames = []
        self.create_new_word_frame()
        
        self.scrollcanvas.configure(height=word_frame_height)
        self.scrollbar.configure(height=word_frame_height)
        self.activateScrollbar()
        self.scrollcanvas.yview_scroll(100, 'pages')
        #self.deactivateScrollbar?
        
        self.is_game_over = False
    
    
    def activateScrollbar(self):
        self.scrollbar.configure(command=self.scrollcanvas.yview, hover=True)
        self.scrollcanvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollcanvas.bind('<Configure>', self.scrollcanvas.configure(scrollregion=self.scrollcanvas.bbox('all')))
    
    
    def deactivateScrollbar(self):
        self.scrollbar.configure(command=None, hover=False)
    
    
    def create_new_word_frame(self):
        
        self.word_frames.append(WordFrame(container=self.scrollwindow))
        self.word_frames[-1].grid(row=len(self.word_frames), column=1, padx=10)
        
        self.scrollwindow.update()
        self.scrollcanvas.update()
        
        if len(self.word_frames) >= inbetween_frames: # NOTE: this is executed every time you enter a new word, see if it will only run ones
            self.activateScrollbar()
            print('scrollbar', self.scrollbar.get())
        
        self.scrollcanvas.configure(height=min((inbetween_frames-0.5)*word_frame_height, self.scrollwindow.winfo_height()))
        self.scrollbar.configure(height=self.scrollcanvas.winfo_height())
        
        words.append('')
    
    
    def delete_last_word_frame(self):
        
        if len(self.word_frames) <= 1:
            return
        
        self.word_frames.pop(-1).destroy()
        words.pop(-1)
        
        self.word_frames[-1].uncolour()
        
        self.scrollwindow.update() # necesarry for resizing
        
        self.scrollcanvas.bind('<Configure>', self.scrollcanvas.configure(scrollregion=self.scrollcanvas.bbox('all')))
        
        if len(self.word_frames) == inbetween_frames-1:
            self.deactivateScrollbar()
        
        if len(self.word_frames) < inbetween_frames:
            self.scrollcanvas.configure(height=len(self.word_frames)*word_frame_height)
            self.scrollbar.configure(height=self.scrollwindow.winfo_height())
    
    
    def end_game(self):
        self.is_game_over = True
    
    
    def update(self):
        self.word_frames[-1].update()
        if len(self.word_frames) > 1:
            self.word_frames[-2].colour()
    
    
    def key_press(self, key):
        # print('key_press: ', key, type(key))
        global words # may not be necessary
        
        key_char = key.char.lower()
        key_code = key.keycode
        
        if(self.is_game_over):
            self.new_game()
            return
        
        if key_char == '\r': #ENTER
            print(words)
            if len(words[-1]) < 4:
                self.post_message("Not a four letter word")
            else:
                if (len(words) == 1 and words[-1] == start_word) or (len(words) > 1 and words[-1] == words[-2]):
                    self.post_message('No Letters Have Been Changed')
                elif not ((len(words) == 1 and self.differs_by_one(words[-1], start_word)) or (len(words) > 1 and self.differs_by_one(words[-1], words[-2]))):
                    self.post_message('More than one letter different')
                elif not self.in_dictionary(words[-1]):
                    self.post_message('Not a word in dictionary')
                elif words[-1] == end_word:
                    self.post_message('You Win! Score = ' + str(len(self.word_frames)), 10_000)
                    self.word_frames[-1].colour()
                    self.end_word_frame.colour()
                    self.end_game()
                else:
                    self.post_message('Next Word')
                    self.create_new_word_frame()
            
        elif key_code == 8: #BACKSPACE
            if len(words[-1]) > 0:
                words[-1] = words[-1][:-1]
            else:
                self.delete_last_word_frame()
        elif key_code > 64 and key_code < 91: #characters a-z
            
            if len(words[-1]) < 4:
                words[-1] += key_char
            
        self.update()
        
        #Scroll to bottom of screen
        self.scrollcanvas.yview_moveto(0.9)
    
    
    def mouse_wheel(self, event):
        if len(self.word_frames) >= inbetween_frames:
            self.scrollcanvas.yview_scroll(-int(event.delta/abs(event.delta)), 'units')
    
    
    def differs_by_one(self, word1, word2):
        differ = 0
        for i in range(4):
            if not word1[i] == word2[i]:
                differ += 1
        return differ == 1
    
    
    # check if word is in dictionary. only searches words in dictionary starting with the same first letter as the submitted word (better efficiency)
    def in_dictionary(self, word):
        global letter_index
        global four_letter_words
        
        start_char = word[0]
        start_index = letter_index[start_char]
        next_char = chr(ord(start_char)+1)
        next_char_index = letter_index[next_char]
        
        return word + "\n" in four_letter_words[start_index:next_char_index]
    
    
    def post_message(self, string, time=5000):
        self.message_label.configure(text=string)
        self.message_label.after(time, lambda: self.message_label.configure(text=''))


if __name__ == "__main__":
    
    
    #### Move this precompute section to LoadGraph.py??
    file = open('DataFiles/fourletterwordlist.txt')
    four_letter_words = file.readlines()
    file.close()
    
    ######### precompute indices of each letter, allows for faster search later on (probably insignificant performance boost)
    
    # letter_index = {'a' : 0}
    # for i in range(1, len(four_letter_words)):
    #     if four_letter_words[i][0] != four_letter_words[i-1][0]:
    #         letter_index[four_letter_words[i][0]] = i
    # letter_index['{'] = len(four_letter_words)
    
    g = LoadGraph()
    
    letter_index = g.load_indices()
    
    start_node, end_node, shortest_paths = g.get_new_game()
    
    start_word = four_letter_words[start_node][:-1]
    end_word = four_letter_words[end_node][:-1]
    
    main = Main()
    main.mainloop()
    