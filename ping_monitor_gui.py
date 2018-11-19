import subprocess
import sys
import tkinter as tk
import threading

class Task(threading.Thread):
    def __init__(self, app, cmd):
        threading.Thread.__init__(self)
        self.app = app
        self.cmd = cmd

    def run(self):
        DETACHED_PROCESS = 0x00000008
        self.app.popen = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, universal_newlines=True, creationflags=DETACHED_PROCESS)
        for datum in iter(self.app.popen.stdout.readline, ''):
            if 'time=' in datum:
                ping = int(datum.partition('time=')[2].partition('ms')[0])
                wide = int(self.app.parent.winfo_width() * min(ping, self.app.limit) / self.app.limit)
                half = self.app.limit/2
                green,red = 'FF',hex(255-int(255*abs(min(ping, self.app.limit) - half)/half))[2:]
                if ping > self.app.limit/2:
                    green,red = red,green
                color = f'#{red:0>2}{green:0>2}00'
                self.app.canvas.itemconfig(self.app.meter, outline=color, fill=color)
                self.app.canvas.coords(self.app.meter, 0,0, wide,self.app.parent.winfo_height())
            elif 'timed out' in datum:
                self.app.canvas.itemconfig(self.app.meter, outline='black', fill='black')
                self.app.canvas.coords(self.app.meter, 0,0, self.app.parent.winfo_width(),self.app.parent.winfo_height())
        self.app.popen.stdout.close()

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
        cmd = ['ping', '-t', *(sys.argv[1:] or ['www.google.com'])]
        self.thread = Task(self, cmd)
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