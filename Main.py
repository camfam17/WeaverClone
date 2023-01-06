from customtkinter import *
from LoadGraph import LoadGraph as lg
#Arch1

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
            tile = CTkLabel(master=self, text=self.static_word[i], font=font1, bg_color='grey', width=75, height=75)
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
    
    
    def move(self, new_command):
        self.configure(command=new_command)


class Main(CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("WeaverClone")
        # self.geometry('380x600')
        self.geometry('420x600')
        self.bind('<Key>', self.key_press)
        
        #TODO: add scroll frame
        
        self.start_word_frame = WordFrame(self, static_word=start_word)
        self.start_word_frame.grid(row=0, column=1)
        self.start_word_frame.colour()
        self.end_word_frame = WordFrame(self, static_word=end_word)
        self.end_word_frame.grid(row=100, column=1)
        
        
        self.word_frames = []
        
        # self.create_new_word_frame()
        
        mainframe = CTkFrame(master=self, width=450)
        mainframe.grid(row=1, column=1)
        
        scrollcanvas = CTkCanvas(master=mainframe)
        scrollcanvas.grid(row=1, column=1)
        scrollbar = CTkScrollbar(master=mainframe, command=scrollcanvas.yview)
        scrollbar.grid(row=1, column=100)
        scrollcanvas.configure(yscrollcommand=scrollbar.set)
        scrollcanvas.bind('<Configure>', lambda e: scrollcanvas.configure(scrollregion=scrollcanvas.bbox('all')))
        
        scrollwindow = CTkFrame(master=scrollcanvas)
        scrollcanvas.create_window((0, 0), window=scrollwindow, anchor='nw')
        testwordframes = []
        for i in range(10):
            testwordframes.append(WordFrame(container=scrollwindow))
            testwordframes[-1].grid(row=i, column=1)
        
        
        self.message_label = CTkLabel(master=self, text='', width=100, height=50)
        self.message_label.grid(row=101, column=1)
        
    
    
    def addScrollbar(self):
        
        self.scrollbar = CTkScrollbar(master=self, width=30, height=300)
        for frame in self.word_frames:
            # frame.configure(master=self.scrollbar)
            # frame.move(self.scrollbar.set)
            frame.config(command=self.scrollbar.set)
        
        self.scrollbar.grid(row=99, column=1)

    
    def create_new_word_frame(self):
        
        self.word_frames.append(WordFrame(self))
        self.word_frames[-1].grid(row=len(self.word_frames), column=1)
        
        # if len(self.word_frames) >= 4:
        #     self.addScrollbar()
        # dwdd
        global words
        words.append('')
    
    
    def delete_last_word_frame(self):
        
        if len(self.word_frames) > 1:
            self.word_frames.pop(-1).destroy()
            words.pop(-1)
            
            self.word_frames[-1].uncolour()
    
    
    def update(self):
        
        self.word_frames[-1].update()
        
        if len(self.word_frames) > 1:
            self.word_frames[-2].colour()
        
    
    
    def key_press(self, key):
        # print('key_press: ', key)
        global words
        
        
        if key.char == '\r': #ENTER
            print(words[-1])
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
                    self.post_message('You Win! Score =' + str(len(self.word_frames)))
                    self.word_frames[-1].colour()
                    self.end_word_frame.colour()
                else:
                    self.post_message('Next Word')
                    self.create_new_word_frame()
            
        elif key.keycode == 8: #BACKSPACE
            if len(words[-1]) > 0:
                words[-1] = words[-1][:-1]
            else:
                self.delete_last_word_frame()
        elif key.keycode > 64 and key.keycode < 91: #characters a-z
            
            if len(words[-1]) < 4:
                words[-1] += key.char
            
        
        print(words)
        self.update()
    
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
        # print('start_char:', start_char, 'start_index:', start_index, 'next_char:', next_char, 'next_char_index:', next_char_index)
        
        return word + "\n" in four_letter_words[start_index:next_char_index]
    
    
    def post_message(self, string, time=5000):
        
        self.message_label.configure(text=string)
        self.message_label.after(time, lambda: self.message_label.configure(text=''))
        
    

if __name__ == "__main__":
    
    # start_word = 'loop'
    # end_word = 'stop'
    
    file = open('fourletterwordlist3.txt')
    four_letter_words = file.readlines()
    file.close()
    
    
    # precompute indices of each letter, allows for faster search later on
    letter_index = {'a' : 0}
    for i in range(1, len(four_letter_words)):
        if four_letter_words[i][0] != four_letter_words[i-1][0]:
            letter_index[four_letter_words[i][0]] = i
    print(letter_index)
    
    g = lg()
    start_node, end_node, shortest_path, shortest_paths = g.get_new_game()
    
    start_word = four_letter_words[start_node][:-1]
    end_word = four_letter_words[end_node][:-1]
    
    # start_word = 'loop'
    # end_word = 'stop'
    
    #TODO: choose start and end words
    # 1) need an algorithm to find optimal path (graph theory?)
    # 2) choose two random words and find shortest path between them OR:
    # 3) chose a start/end word and word your way forwards/backwards to get the end/start word respectively (may be pointless since you need to find optimal path anyway) OR:
    # 4) select a minimum number of guesses x you want the user to make. select a random start word and traverse their adjacent nodes x times to get x guesses away from the start word
    # 5) create a visual graph of all the words and their adjacent nodes, show all paths from start word to end word (under certain number of guesses), look for graph visualization packages/modules
    
    main = Main()
    main.mainloop()
    