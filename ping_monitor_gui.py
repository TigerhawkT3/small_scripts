import subprocess
import sys
import tkinter as tk
import threading

class App:
    def __init__(self, parent):
        self.parent = parent
        self.limit = 1000
        self.canvas = tk.Canvas(parent)
        self.canvas.pack(fill='both', expand=True)
        self.borderless = False
        self.topmost = False
        parent.bind('<Shift-Return>', self.make_topmost)
        parent.bind('<Alt-Return>', self.remove_borders)
        parent.bind('<Escape>', self.end)
        self.meter = self.canvas.create_rectangle(0,0, self.parent.winfo_width(),self.parent.winfo_height(), fill='black')
        def ping():
            DETACHED_PROCESS = 8
            cmd = ['ping', '-t', *(sys.argv[1:] or ['www.google.com'])]
            self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, creationflags=DETACHED_PROCESS)
            for datum in iter(self.popen.stdout.readline, ''):
                if 'time=' in datum:
                    ping = int(datum.partition('time=')[2].partition('ms')[0])
                    wide = int(self.parent.winfo_width() * min(ping, self.limit) / self.limit)
                    half = self.limit/2
                    green,red = 'FF',hex(255-int(255*abs(min(ping, self.limit) - half)/half))[2:]
                    if ping > self.limit/2:
                        green,red = red,green
                    color = f'#{red:0>2}{green:0>2}00'
                    self.canvas.itemconfig(self.meter, outline=color, fill=color)
                    self.canvas.coords(self.meter, 0,0, wide,self.parent.winfo_height())
                elif 'timed out' in datum:
                    self.canvas.itemconfig(self.meter, outline='black', fill='black')
                    self.canvas.coords(self.meter, 0,0, self.parent.winfo_width(),self.parent.winfo_height())
            self.popen.stdout.close()
        self.thread = threading.Thread()
        self.thread.run = ping
        self.thread.start()
        self.update()
    def update(self):
        if self.thread.isAlive():
            self.parent.after(500, self.update)
    def end(self, event=None):
        self.popen.terminate()
        self.parent.destroy()
    def remove_borders(self, event=None):
        self.topmost = not self.topmost
        self.parent.overrideredirect(self.topmost)
    def make_topmost(self, event=None):
        self.borderless = not self.borderless
        self.parent.wm_attributes('-topmost', self.borderless)
        
if __name__ == '__main__':        
    root = tk.Tk()
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.end)
    root.mainloop()