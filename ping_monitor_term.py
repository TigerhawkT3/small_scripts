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

class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        stdscr.timeout(0)
        self.char = '▓'
        self.limit = 1000
        self.height, self.width = stdscr.getmaxyx()
        self.pad = curses.newpad(self.height+1, self.width+1)
        curses.init_pair(1, 1, 1)
        stdscr.clear()
        data = ping_stream(['ping', '-t', *(sys.argv[1:] or ['www.google.com'])])
        # test data:
        #data = [f'time={t}ms' for t in range(0,1501, 100)]; data.insert(6, 'timed out')
        self.process(data)
    def process(self, data):
        for datum in data:
            if self.stdscr.getch() != -1:
                break
            self.pad.clear()
            if 'time=' in datum:
                ping = int(datum.partition('time=')[2].partition('ms')[0])
                half = self.limit/2
                green,red = 1000,1000-int(1000*abs(min(ping, self.limit) - half)/half)
                if ping > self.limit/2:
                    green,red = red,green
                curses.init_color(1, red, green, 0) # color #1, up to 1000 of each channel
                fill = self.char * int(self.width * min(ping, self.limit) / self.limit) + '\n'
                self.pad.addstr((fill * self.height).strip(), curses.color_pair(1))
                self.pad.refresh(0,0, 0,0, self.height-1,self.width-1)
            elif 'timed out' in datum:
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                self.pad.refresh(0,0, 0,0, self.height-1,self.width-1)
                for _ in range(3):
                    curses.flash()
                    curses.napms(50)
                curses.init_pair(1, 1, 1)
        # with test data:
        #    curses.napms(1500)
        #self.stdscr.timeout(-1)
        #self.stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(App)