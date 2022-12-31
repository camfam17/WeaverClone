from customtkinter import *


class WordFrame(CTkFrame):
    
    def __init__(self, container):
        super().__init__(container)
        
        tiles = []
        for i in range(4):
            tile = CTkLabel(master = self, text = str(i), width=50, height=50)
            tiles.append(tile)
            tiles[-1].grid(row=1, column=i*50, padx=10, pady=10)


class Main(CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("WeaverClone")
        self.bind('<Key>', self.key_press)
        
        self.word_frame = WordFrame(self)
        self.word_frame.grid(row=0, column=0)
    
    def key_press(self, key):
        print('key_press: ', key)

if __name__ == "__main__":
    main = Main()
    main.mainloop()