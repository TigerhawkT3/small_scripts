from matrix_rotation import rotate_array as rot
import sys

names = {'B':'Player 1', 'R':'Player 2'}

if len(sys.argv) == 3:
    names['B'] = sys.argv[1]
    names['R'] = sys.argv[2]

board = [list('*'*7) for i in range(6)]

def askmove(piece):
    for row in board:
        print(*row, sep='')
    
    while 1:
        try:
            move = int(input('\n> ')[0])
        except (ValueError, IndexError):
            pass
        else:
            if move in range(len(board[0])) and board[0][move] == '*':
                break
    
    column = [row[move] for row in board][::-1]
    index = column.index('*')
    board[-index-1][move] = piece
    left = rot(board, 45, wide=True)
    right = rot(board, 315, wide=True)
    sideways = rot(board, 90, wide=True)
    if any(piece*4 in ''.join(row) for array in (board, left, right, sideways) for row in array):
        print('{} wins with {}!'.format(names[piece], piece))
    elif all(p != '*' for row in board for p in row):
        print('Tie.')
    else:
        return True

while askmove('B') and askmove('R'):
    pass