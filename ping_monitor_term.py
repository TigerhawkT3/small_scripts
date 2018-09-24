import curses
import subprocess
import sys

def ping_stream(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    yield from iter(popen.stdout.readline, '')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def update(*windows):
    for window in windows:
        window.noutrefresh()
    curses.doupdate()

class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        stdscr.timeout(0)
        self.char = '▓'
        self.limit = 1000
        self.height, self.width = stdscr.getmaxyx()
        pad = self.pad = curses.newpad(self.height+1, self.width+1)
        self.pairs = [(curses.COLOR_GREEN, curses.COLOR_GREEN),
                      (curses.COLOR_YELLOW, curses.COLOR_YELLOW),
                      (curses.COLOR_MAGENTA, curses.COLOR_MAGENTA),
                      (curses.COLOR_RED, curses.COLOR_RED)]
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()
        self.pad.addstr(self.char * ((self.height * self.width)-1),
                           curses.color_pair(1))
        self.pad.insch(ord(self.char), curses.color_pair(1))
        stdscr.refresh()
        pad.refresh(0,0, 0,0, self.height-1,self.width-1)
        data = ping_stream(['ping', '-t', *(sys.argv[1:] or ['www.google.com'])])
        #data = [f'time={t}ms' for t in (0,0,50,150,250,350,1100,900)]; data.insert(6, 'timed out')
        self.process(data)
    def process(self, data):
        data = iter(data)
        next(data); next(data) # skip the header
        for datum in data:
            if self.stdscr.getch() != -1:
                break
            self.pad.clear()
            if 'time=' in datum:
                ping = int(datum.partition('time=')[2].partition('ms')[0])
                fill = self.char * int(self.width * min(ping, self.limit) / self.limit) + '\n'
                self.pad.addstr((fill * self.height).strip(), curses.color_pair(1))
                curses.init_pair(1, *self.pairs[min(ping//100, len(self.pairs)-1)])
                self.pad.refresh(0,0, 0,0, self.height-1,self.width-1)
            elif 'timed out' in datum:
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                self.pad.refresh(0,0, 0,0, self.height-1,self.width-1)
                for _ in range(3):
                    curses.flash()
                    curses.napms(50)
                curses.init_pair(1, *self.pairs[-1])
        # with test data:
        #    curses.napms(1500)
        #self.stdscr.timeout(-1)
        #self.stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(App)