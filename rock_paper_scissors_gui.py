import tkinter as tk
import rock_paper_scissors as rps

class RPS:
    def __init__(self, parent):
        self.parent = parent
        self.difficulty = 'e'
        self.difficulties = {dif.lower()[0]:tk.Button(
                                    root, width=10, text=dif,
                                    command=lambda dif=dif: self.set_difficulty(dif.lower()[0]))
                         for dif in ('Easy', 'Medium', 'Hard')
                       }
        self.choices = {c.lower()[0]:tk.Button(
                                    root, width=10, text=c,
                                    command=lambda c=c:self.status.config(
                                            text=rps.win(c.lower()[0], self.difficulty)))
                         for c in ('Rock', 'Paper', 'Scissors')
                       }
        self.status = tk.Label(root, text='Click to play!')
        ordering = {'e':0, 'm':1, 'h':2, 'r':0, 'p':1, 's':2}
        for idx,d in enumerate((self.difficulties, self.choices)):
            for k in sorted(d, key=ordering.get):
                d[k].grid(row=idx, column=ordering[k])
        self.status.grid(row=3, column=0, columnspan=3)
    
    def set_difficulty(self, d):
        self.difficulty = d
    
root = tk.Tk()
game = RPS(root)
root.mainloop()