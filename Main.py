from customtkinter import *
#Arch1

words = []
class WordFrame(CTkFrame):
    
    def __init__(self, container, **kwargs):
        super().__init__(container)
        
        try:
            self.static_word = kwargs['static_word']
        except KeyError:
            self.static_word = '    '
        
        self.tiles = []
        for i in range(4):
            tile = CTkLabel(master=self, text=self.static_word[i], bg_color='grey', width=50, height=50)
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
        self.bind('<Key>', self.key_press)
        
        #TODO: add scroll frame
        
        self.start_word_frame = WordFrame(self, static_word=start_word)
        self.start_word_frame.grid(row=0, column=1)
        self.end_word_frame = WordFrame(self, static_word=end_word)
        self.end_word_frame.grid(row=100, column=1)
        
        
        self.word_frames = []
        
        self.create_new_word_frame()
        
        self.message_label = CTkLabel(master=self, text='', width=100, height=50)
        self.message_label.grid(row=101, column=1)
        
    
    
    def create_new_word_frame(self):
        
        self.word_frames.append(WordFrame(self))
        self.word_frames[-1].grid(row=len(self.word_frames), column=1)
        
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
        print('key_press: ', key)
        global words
        
        if key.char == '\r': #ENTER
            
            if len(words[-1]) < 4:
                self.post_message("Not a four letter word")
            else:
                if words[-1] == end_word:
                    self.post_message('You Win! Score =' + str(len(self.word_frames)))
                    self.word_frames[-1].colour()
                    self.end_word_frame.colour()
                elif (len(words) == 1 and words[-1] == start_word) or (len(words) > 1 and words[-1] == words[-2]):
                    self.post_message('No Letters Have Been Changed')
                elif not ((len(words) == 1 and self.differs_by_one(words[-1], start_word)) or (len(words) > 1 and self.differs_by_one(words[-1], words[-2]))):
                    self.post_message('More than one letter different')
                elif not self.in_dictionary(words[-1]):
                    self.post_message('Not a word in dictionary')
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
            
        
        self.update()
    
    def differs_by_one(self, word1, word2):
        
        differ = 0
        for i in range(4):
            if not word1[i] == word2[i]:
                differ += 1
        
        return differ == 1
    
    def in_dictionary(self, word):
        global letter_index
        global four_letter_words
        
        start_index = letter_index[word[0]]
        end_char = chr(ord([*word][0])+1)
        end_index = letter_index[end_char]
        print('start_index:', start_index, 'end_char:', (end_char), 'end_index:', end_index)
        
        return word + "\n" in four_letter_words[start_index:end_index]
    
    def post_message(self, string, time=5000):
        
        self.message_label.configure(text=string)
        self.message_label.after(time, lambda: self.message_label.configure(text=''))
        
    

if __name__ == "__main__":
    
    start_word = 'loop'
    end_word = 'stop'
    
    
    four_letter_words = (open('fourletterwordlist1.txt')).readlines()
    letter_index = {'a' : 0}
    
    # precompute indices of each letter, allows for faster search later on
    for i in range(1, len(four_letter_words)):
        if four_letter_words[i][0] != four_letter_words[i-1][0]:
            letter_index[four_letter_words[i][0]] = i
    
    #TODO: choose start and end words
    # 1) need an algorithm to find optimal path (graph theory?)
    # 2) choose two random words and find shortest path between them OR:
    # 3) chose a start/end word and word your way forwards/backwards to get the end/start word respectively (may be pointless since you need to find optimal path anyway) OR:
    # 4) select a minimum number of guesses x you want the user to make. select a random start word and traverse their adjacent nodes x times to get x guesses away from the start word
    # 5) create a visual graph of all the words and their adjacent nodes, show all paths from start word to end word (under certain number of guesses), look for graph visualization packages/modules
    
    main = Main()
    main.mainloop()
    