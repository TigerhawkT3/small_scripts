import subprocess
import sys
import tkinter as tk

def ping_stream(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    yield from iter(popen.stdout.readline, '')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

class App:
    def __init__(self, parent):
        self.parent = parent
        self.height,self.width = 300,1000
        self.limit = 1000
        self.canvas = tk.Canvas(parent, height=self.height, width=self.width)
        self.canvas.pack()
        parent.bind('<space>', lambda event=None: parent.destroy())
        parent.bind('<Escape>', lambda event=None: parent.destroy())
        parent.bind('<Return>', lambda event=None: parent.destroy())
        self.meter = self.canvas.create_rectangle(0,0, self.width,self.height, fill='black')
        self.data = iter(ping_stream(['ping', '-t', *(sys.argv[1:] or ['www.google.com'])]))
        # test data - increase after() call for delay
        #self.data = [f'time={t}ms' for t in range(0,1501, 100)]
        #self.data.insert(6, 'timed out')
        #self.data = iter(self.data)
        self.process()
    def process(self):
        try:
            datum = next(self.data)
        except StopIteration:
            return
        if 'time=' in datum:
            ping = int(datum.partition('time=')[2].partition('ms')[0])
            wide = int(self.width * min(ping, self.limit) / self.limit)
            half = self.limit/2
            green,red = 'FF',hex(255-int(255*abs(min(ping, self.limit) - half)/half))[2:]
            if ping > self.limit/2:
                green,red = red,green
            color = f'#{red:0>2}{green:0>2}00'
            self.canvas.itemconfig(self.meter, outline=color, fill=color)
            self.canvas.coords(self.meter, 0,0, wide,self.height)
        elif 'timed out' in datum:
            self.canvas.itemconfig(self.meter, outline='black', fill='black')
            self.canvas.coords(self.meter, 0,0, self.width,self.height)
        self.parent.after(1, self.process)
        
if __name__ == '__main__':        
    root = tk.Tk()
    app = App(root)
    root.mainloop()