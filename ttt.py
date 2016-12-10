board = [['*' for i in range(3)] for j in range(3)]

def askmove(piece):
    while True:
        try:
            x,y = map(int, input('\n> '))
            if board[x-1][y-1] == '*':
                board[x-1][y-1] = piece
            else:
                continue
        except (ValueError, IndexError):
            pass
        else:
            break
    print('', *(' '.join(row) for row in board), sep='\n')
    if ([piece] * 3 in board or
        (piece,) * 3 in zip(*board) or
        all(board[i][i] == piece for i in range(3)) or
        all(board[i][2-i] == piece for i in range(3))):
        print(piece, 'wins.')
    elif all(p!='*' for row in board for p in row):
        print('Tie.')
    else:
        return True
    
while askmove('X') and askmove('O'):
    pass