import subprocess
import sys
import tkinter as tk
import threading

class App:
    def __init__(self, parent):
        self.parent = parent
        parent.title('Ping monitor by TigerhawkT3')
        self.limit = 1000
        self.canvas = tk.Canvas(parent, highlightthickness=0, bd=0, bg='white')
        self.canvas.pack(fill='both', expand=True)
        self.borderless = False
        self.opaque = True
        self.topmost = False
        parent.bind('<Alt-Return>', self.remove_borders)
        parent.bind('<Shift-Return>', self.make_opaque)
        parent.bind('<Control-Return>', self.make_topmost)
        for i in range(10):
            parent.bind(f'{i}', lambda event=None, i=i: self.parent.attributes('-alpha', i/10 or 1))
            parent.bind(f'KP_{i}', lambda event=None, i=i: self.parent.attributes('-alpha', i/10 or 1))
        self.orientation = ['L']
        for key in ('Up', 'Down', 'Left', 'Right'):
            parent.bind(f'<{key}>', lambda event=None, key=key[0]: self.orientation.__setitem__(0, key))
        self.slim = [False]
        self.slim_width = 5
        parent.bind('<BackSpace>', lambda event=None: self.slim.__setitem__(0, (not self.slim[0])*self.slim_width))
        parent.bind('<Escape>', self.end)
        self.meter = self.canvas.create_rectangle(0,0, self.parent.winfo_width()-1,self.parent.winfo_height()-1, fill='black')
        def ping():
            DETACHED_PROCESS = 8
            cmd = ['ping', '-t', *(sys.argv[1:] or ['www.google.com'])]
            self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, creationflags=DETACHED_PROCESS)
            for datum in iter(self.popen.stdout.readline, ''):
                if 'time=' in datum:
                    w,h = self.parent.winfo_width()-1,self.parent.winfo_height()-1
                    ping = int(datum.partition('time=')[2].partition('ms')[0])
                    half = self.limit/2
                    green,red = 'FF',hex(255-int(255*abs(min(ping, self.limit) - half)/half))[2:]
                    if ping > self.limit/2:
                        green,red = red,green
                    color = f'#{red:0>2}{green:0>2}00'
                    self.canvas.itemconfig(self.meter, outline=color, fill=color)
                    if self.orientation[0] == 'L':
                        x1,y1, x2,y2 = 0,0, self.find_size(w, ping),h
                    elif self.orientation[0] == 'R':
                        x1,y1, x2,y2 = w-self.find_size(w, ping),0, w,h
                    elif self.orientation[0] == 'U':
                        x1,y1, x2,y2 = 0,0, self.slim[0] or w,self.find_size(h, ping)
                    elif self.orientation[0] == 'D':
                        x1,y1, x2,y2 = 0,h-self.find_size(h, ping), self.slim[0] or w,h
                    self.canvas.coords(self.meter, x1,y1, x2,y2)
                elif 'timed out' in datum:
                    self.canvas.itemconfig(self.meter, outline='black', fill='black')
                    self.canvas.coords(self.meter, 0,0, self.parent.winfo_width(),self.parent.winfo_height())
            self.popen.stdout.close()
        self.thread = threading.Thread()
        self.thread.run = ping
        self.thread.start()
        self.update()
        for _ in range(2):
            self.make_opaque()
            self.remove_borders()
    def update(self):
        if self.thread.isAlive():
            self.parent.after(500, self.update)
    def end(self, event=None):
        self.popen.terminate()
        self.parent.destroy()
    def remove_borders(self, event=None):
        self.borderless = not self.borderless
        self.parent.overrideredirect(self.borderless)
    def make_topmost(self, event=None):
        self.topmost = not self.topmost
        self.parent.attributes('-topmost', self.topmost)
    def make_opaque(self, event=None):
        self.opaque = not self.opaque
        if sys.platform == 'win32': # windows
            self.parent.attributes('-transparentcolor', ('white', '')[self.opaque])
        elif sys.platform == 'darwin': # mac
            self.parent.attributes('-transparent', not self.opaque)
            self.parent.config(bg=('systemTransparent', '')[self.opaque])
            self.canvas.config(bg=('systemTransparent', 'white')[self.opaque])
    def find_size(self, dimension, ping):
        return int(dimension * min(ping, self.limit) / self.limit)
        
if __name__ == '__main__':        
    root = tk.Tk()
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.end)
    root.mainloop()