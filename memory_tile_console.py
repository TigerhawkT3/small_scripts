import random
import time

answer = list('AABBCCDDEEFFGGHH')
random.shuffle(answer)
answer = [answer[:4],
         answer[4:8],
         answer[8:12],
         answer[12:]]
board = [list('*'*4) for i in range(4)]

def choose():
    a,b = map(int, input('? '))
    show_board((a,b))
    x,y = map(int, input('? '))
    show_board((a,b),(x,y))
    if answer[a][b] == answer[x][y]:
        print('Matched!')
        board[a][b] = answer[a][b]
        board[x][y] = answer[x][y]
    else:
        print('Not a match.')
    if any('*' in row for row in board):
        return True
    
def show_board(*tiles):
    for row in range(len(answer)):
        for column in range(len(answer[0])):
            if (row,column) in tiles:
                print(answer[row][column].lower(), end='', flush=True)
            else:
                print(board[row][column], end='', flush=True)
        print()

show_board()
t = time.monotonic()
while choose():
    pass

print('Done! Time:', time.monotonic()-t)