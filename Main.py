from customtkinter import *
#Arch1

words = []
class WordFrame(CTkFrame):
    
    def __init__(self, container):
        super().__init__(container)
        
        self.tiles = []
        for i in range(4):
            tile = CTkLabel(master = self, text = str(i), width=50, height=50)
            self.tiles.append(tile)
            self.tiles[-1].grid(row=1, column=i*50, padx=10, pady=10)
    
    
    def update(self):
        
        for i in range(4):
            if i < len(words[-1]):
                self.tiles[i].configure(text=words[-1][i])
            else:
                self.tiles[i].configure(text=str(i))


class Main(CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("WeaverClone")
        self.bind('<Key>', self.key_press)
        
        self.current_word = ''
        global words
        words.append(self.current_word)
        self.word_frames = []
        
        self.create_new_word_frame()
        
        
    
    
    def create_new_word_frame(self):
        
        self.word_frames.append(WordFrame(self))
        self.word_frames[-1].grid(row=len(self.word_frames), column=1)
        
        global words
        words.append('')
        print(len(self.word_frames))
    
    def update(self):
        
        self.word_frames[-1].update()
        
    
    def key_press(self, key):
        print('key_press: ', key)
        global words
        
        if key.char == '\r': #ENTER
            
            if len(words[-1]) == 4:
                self.create_new_word_frame()
        
        elif key.keycode == 8: #BACKSPACE
            if len(words[-1]) > 0:
                words[-1] = words[-1][:-1]
            else:
                if len(self.word_frames) > 1:
                    self.word_frames.pop(-1).destroy()
                    words.pop(-1)
        elif key.keycode > 64 and key.keycode < 91: #a-z
            
            if len(words[-1]) < 4:
                words[-1] += key.char
            
        
        self.update()

if __name__ == "__main__":
    main = Main()
    main.mainloop()