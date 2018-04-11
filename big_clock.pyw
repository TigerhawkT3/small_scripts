import tkinter as tk
from datetime import datetime

class Time:
    def __init__(self, parent):
        self.parent = parent
        w, h = 1200, 700
        self.canvas = tk.Canvas(root, width=w, height=h)
        self.canvas.pack()
        self.text = self.canvas.create_text(w//2,h//2, font=('Consolas', 250, 'bold'))
        self.update()
    def update(self):
        self.canvas.itemconfig(self.text, text=datetime.now().strftime('%m/%d\n%H:%M'))
        self.parent.after(15_000, self.update)

root = tk.Tk()
mytime = Time(root)
root.mainloop()