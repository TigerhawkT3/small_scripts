import tkinter as tk
import random
import collections

class Mastermind:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(parent)
        self.status = tk.Label(parent)
        self.draw_board()
    def draw_board(self, event=None):
        self.canvas.destroy()
        self.status.destroy()
        self.canvas = tk.Canvas(self.parent, width=400, height=1027)
        self.canvas.pack()
        self.bag = {'r':self.canvas.create_oval(0, 960, 66, 1027, fill='red', outline='red'),
                    'o':self.canvas.create_oval(66, 960, 131, 1027, fill='orange', outline='orange'),
                    'y':self.canvas.create_oval(131, 960, 200, 1027, fill='yellow', outline='yellow'),
                    'g':self.canvas.create_oval(200, 960, 267, 1027, fill='green', outline='green'),
                    'b':self.canvas.create_oval(267, 960, 334, 1027, fill='blue', outline='blue'),
                    'p':self.canvas.create_oval(334, 960, 400, 1027, fill='purple', outline='purple')
                   }
        self.ids = {v:k for k,v in self.bag.items()}
        self.colors = {'r':'red', 'o':'orange', 'y':'yellow',
                       'g':'green', 'b':'blue', 'p':'purple'}
        self.guesses = ['']
        self.status = tk.Label(self.parent)
        self.status.pack()
        self.canvas.bind('<1>', self.check)
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Control-N>', self.draw_board)
        self.pattern = [random.choice('roygbp') for _ in range(4)]
        self.counted = collections.Counter(self.pattern)
    def check(self, event=None):
        id = self.canvas.find_withtag("current")[0]
        guess = self.ids[id]
        self.guesses[-1] += guess
        x_offset = (len(self.guesses[-1]) - 1) * 80
        y_offset = (len(self.guesses) - 1) * 80
        self.canvas.create_oval(x_offset, y_offset,
                                x_offset+80, y_offset+80,
                                fill=self.colors[guess],
                                outline=self.colors[guess])
        if len(self.guesses[-1]) < 4:
            return
        guess_count = collections.Counter(self.guesses[-1])
        close = sum(min(self.counted[k], guess_count[k]) for k in self.counted)
        exact = sum(a==b for a,b in zip(self.pattern, self.guesses[-1]))
        close -= exact
        colors = exact*['black'] + close*['white']
        key_coordinates = [(320, y_offset, 360, y_offset+40),
                           (360, y_offset, 400, y_offset+40),
                           (320, y_offset+40, 360, y_offset+80),
                           (360, y_offset+40, 400, y_offset+80)]
        for color, coord in zip(colors, key_coordinates):
            self.canvas.create_oval(coord, fill=color, outline=color)
        if exact == 4:
            self.status.config(text='You win!')
            self.canvas.unbind('<1>')
        elif len(self.guesses) > 11:
            self.status.config(
                               text='Out of guesses. The correct answer is {}.'.format(
                                ''.join(self.pattern)))
            self.canvas.unbind('<1>')
        else:
            self.guesses.append('')
        
root = tk.Tk()
game = Mastermind(root)
root.mainloop()