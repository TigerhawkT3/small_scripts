import tkinter as tk
import random
import collections

class Mastermind:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.draw_board()
    def draw_board(self, event=None):
        self.frame.destroy()
        self.frame = tk.Frame(self.parent)
        self.frame.pack()
        self.guess_fields = [tk.Entry(self.frame) for i in range(12)]
        self.hint_fields = [tk.Label(self.frame, text='----') for i in range(12)]
        for idx, (guess, hint) in enumerate(zip(self.guess_fields, self.hint_fields)):
            guess.grid(row=idx, column=0)
            hint.grid(row=idx, column=1)
        self.status = tk.Label(self.frame, text='Begin!')
        self.status.grid(row=12, column=0, columnspan=2)
        for guess in self.guess_fields:
            guess.config(state=tk.DISABLED)
        self.guess_fields[0].config(state=tk.NORMAL)
        self.guess_fields[0].focus_set()
        self.parent.bind('<Return>', self.check)
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Control-N>', self.draw_board)
        self.current = 0
        self.pattern = [random.choice('abcdef') for _ in range(4)]
        self.counted = collections.Counter(self.pattern)
    def check(self, event=None):
        guess = self.guess_fields[self.current].get()
        guess_count = collections.Counter(guess)
        close = sum(min(self.counted[k], guess_count[k]) for k in self.counted)
        exact = sum(a==b for a,b in zip(self.pattern, guess))
        close -= exact
        hint = exact*'!' + close*'?'
        self.hint_fields[self.current].config(text='{:-<4}'.format(hint))
        self.guess_fields[self.current].config(state=tk.DISABLED)
        self.current += 1
        if exact == 4:
            self.status.config(text='You win!')
        elif self.current > 11:
            self.status.config(
                               text='Out of guesses. The correct answer is {}.'.format(
                                ''.join(self.pattern)))
        else:
            self.guess_fields[self.current].config(state=tk.NORMAL)
            self.guess_fields[self.current].focus_set()
            self.status.config(text='')
        
root = tk.Tk()
game = Mastermind(root)
root.mainloop()