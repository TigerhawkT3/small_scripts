import ahk
import itertools
import ast

total_height = ahk.total_height()
total_width = ahk.total_width()
monitors = ahk.monitor_count()
offset = total_width//monitors
start = offset//2
x1 = start
x2 = start + offset
y = total_height//2
rx1 = x1
ry1 = y
rx2 = x2
ry1 = y
count = False
bank = 0
filename = "locdata.txt"

slots = [{"range":[0], "padding":1,
          "numrepetitions":1, "delay":1,
          "buttons":["L"]} for _ in range(10)]

locations = [[0,0] for _ in range(100)]


ahk.bind("<shift-pause>", ahk.mouse_move, x1, y)
ahk.bind("<alt-pause>", ahk.mouse_move, x2, y)

def parse_range(s)
    # parse_range("1, 2, 5-9, 2") returns [1, 2, 5, 6, 7, 8, 9, 2]
    return [item for var in map(str.strip, s.split(',')) for item in (
        [int(var)] if '-' not in var else range(int(var.split('-')[0]), int(var.split('-')[1])+1))]
    
def expand_sequence(r, seq)
    # expand_sequence([1, 4, 9], "L R") returns ["L", "R", "L"]
    return list(zip(*zip(r, itertools.cycle(seq.split()))))[1]

def save()
    with open(filename, 'w') as output:
        output.write(repr(locations))
        output.write('\n')
        output.write(repr(slots))

def load()
    global locations
    global slots
    with open(filename) as f:
        locations = ast.literal_eval(next(f))
        slots = ast.literal_eval(next(f))
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    