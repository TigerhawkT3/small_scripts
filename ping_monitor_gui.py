import subprocess
import sys
import tkinter as tk
import threading

class PingMonitor:
    def __init__(self, parent):
        '''set up the window, ping command, etc.'''
        self.parent = parent
        self.top = tk.Toplevel()
        self.parent.withdraw()  # remove the main window while the toplevel has borders
        self.top.protocol('WM_DELETE_WINDOW', self.end) # quit gracefully on "X"
        self.parent.title('Ping monitor by TigerhawkT3')
        self.top.title('Ping monitor by TigerhawkT3')
        self.canvas = tk.Canvas(self.top, highlightthickness=0, bd=0, bg='white')
        self.canvas.pack(fill='both', expand=True)
        self.limit = 1000       # when ping is over this many ms, the display is full and red
        self.borderless = False # start with normal window title bar
        self.opaque = True      # start with opaque background
        self.topmost = False    # start without being topmost window
        self.orientation = 'L'  # anchor ping bar at the left
        self.max_width = 0      # max width for vertical display starts unbounded
        self.top.bind('<Alt-Return>', self.remove_borders)
        self.top.bind('<Shift-Return>', self.make_opaque)
        self.top.bind('<Control-Return>', self.make_topmost)
        self.top.bind('<F5>', self.reset_box)
        for i in range(10):     # 0-9 to set window transparency
            self.top.bind(f'{i}', lambda event=None, i=i: self.top.attributes('-alpha', i/10 or 1))
            self.top.bind(f'KP_{i}', lambda event=None, i=i: sself.top.attributes('-alpha', i/10 or 1))
        for key in ('<Up>', '<Down>', '<Left>', '<Right>'):
            self.top.bind(key, self.set_orientation)
        self.canvas.bind('<Button-3>', self.start_box)
        self.canvas.bind('<B3-Motion>', self.update_box)
        self.canvas.bind('<ButtonRelease-3>', self.end_box)
        self.top.bind('<Escape>', self.end)
        def ping():
            '''start a ping command and update the display with each new datum'''
            self.x1, self.y1, self.x2, self.y2 = 0, 0, self.top.winfo_width(), self.top.winfo_height()
            self.meter = self.canvas.create_rectangle(self.x1,self.y1, self.x2,self.y2, fill='black')
            DETACHED_PROCESS = 8 # run the subprocess without a console window
            cmd = ['ping', '-t', *(sys.argv[1:] or ['www.google.com'])]
            self.popen = subprocess.Popen(cmd,
                                          stdout=subprocess.PIPE,
                                          universal_newlines=True,
                                          creationflags=DETACHED_PROCESS)
            for datum in iter(self.popen.stdout.readline, ''):
                if 'time=' in datum:
                    ping = int(datum.partition('time=')[2].partition('ms')[0])
                    half = self.limit/2
                    green,red = 'FF',hex(255-int(255*abs(min(ping, self.limit) - half)/half))[2:]
                    if ping > self.limit/2:
                        green,red = red,green
                    color = f'#{red:0>2}{green:0>2}00'
                    self.canvas.itemconfig(self.meter, outline=color, fill=color)
                    if self.orientation[0] == 'L':
                        x1,y1, x2,y2 = self.x1,self.y1, self.x1+self.find_size(self.x2-self.x1, ping),self.y2
                    elif self.orientation[0] == 'R':
                        x1,y1, x2,y2 = self.x2-self.find_size(self.x2-self.x1, ping),self.y1, self.x2,self.y2
                    elif self.orientation[0] == 'U':
                        x1,y1, x2,y2 = self.x1,self.y1, self.x2,self.y1+self.find_size(self.y2-self.y1, ping)
                    elif self.orientation[0] == 'D':
                        x1,y1, x2,y2 = self.x1,self.y2-self.find_size(self.y2-self.y1, ping), self.x2,self.y2
                    self.canvas.coords(self.meter, x1,y1, x2,y2)
                elif 'timed out' in datum:
                    self.canvas.itemconfig(self.meter, outline='black', fill='black')
                    self.canvas.coords(self.meter, self.x1, self.y1, self.x2, self.y2)
            self.popen.stdout.close()
        self.thread = threading.Thread()    # start a new thread
        self.thread.run = ping              # set the thread's run method to our ping command above
        self.thread.start()                 # start the thread
        self.update()                       # keep checking on the thread and updating the display
        # setting a transparent bg for the first time breaks the window's title bar; this bypasses that
        for _ in range(2):
            self.make_opaque()
            self.remove_borders()
    def update(self):
        '''check on the thread and schedule the next check'''
        if self.thread.isAlive():
            self.parent.after(500, self.update)
    def end(self, event=None):
        '''stop the ping process and close the window'''
        self.popen.terminate()
        self.top.destroy()
        self.parent.destroy()
    def start_box(self, event=None):
        '''begin defining a bounding box for the display.'''
        self.temp_x1, self.temp_y1 = event.x, event.y
        self.box = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='blue')
    def update_box(self, event=None):
        '''update the bounding box guide'''
        self.canvas.coords(self.box, self.temp_x1, self.temp_y1, event.x, event.y)
    def end_box(self, event=None):
        '''complete the definition of a bounding box for the display.'''
        self.x2, self.y2 = event.x, event.y
        self.x1, self.x2 = sorted((self.temp_x1, self.x2))
        self.y1, self.y2 = sorted((self.temp_y1, self.y2))
        self.parent.after(2000, self.canvas.delete, self.box)
    def reset_box(self, event=None):
        '''reset the display area to the window size'''
        self.x1, self.y1, self.x2, self.y2 = 0, 0, self.top.winfo_width(), self.top.winfo_height()
    def set_orientation(self, event=None):
        '''change the orientation to L/R/U/D'''
        self.orientation = event.keysym[0]
    def remove_borders(self, event=None):
        '''toggle the window's title bar, border, etc.'''
        self.borderless = not self.borderless
        # when the toplevel has borders, withdraw the root entirely.
        # when it doesn't, merely iconify the root.
        (self.parent.withdraw, self.parent.iconify)[self.borderless]()
        # when the toplevel has borders, release the grab so it can be minimized.
        # when it's borderless, grab it so the root doesn't barge in.
        (self.top.grab_release, self.top.grab_set)[self.borderless]()
        self.top.overrideredirect(self.borderless) # remove borders
    def make_topmost(self, event=None):
        '''toggle whether the window is always on top'''
        self.topmost = not self.topmost
        self.top.attributes('-topmost', self.topmost)
    def make_opaque(self, event=None):
        '''toggle whether the canvas background is opaque.
        these are system specific and only implemented for windows and mac.'''
        self.opaque = not self.opaque
        if sys.platform == 'win32':     # windows
            self.top.attributes('-transparentcolor', ('white', '')[self.opaque])
        elif sys.platform == 'darwin':  # mac
            self.top.attributes('-transparent', not self.opaque)
            self.top.config(bg=('systemTransparent', '')[self.opaque])
            self.canvas.config(bg=('systemTransparent', 'white')[self.opaque])
    def find_size(self, dimension, ping):
        '''find the size in pixels of the ping bar, given the
        window size (dimension) and the current ping (relative
        to the ping limit)'''
        return int(dimension * min(ping, self.limit) / self.limit)
        
if __name__ == '__main__':        
    root = tk.Tk()
    app = PingMonitor(root)
    root.protocol('WM_DELETE_WINDOW', app.end) # quit gracefully on "X"
    root.mainloop()