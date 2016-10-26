import random

def rand(l=['rock', 'paper', 'scissors']):
    return random.choice(l)
    
def win(player, difficulty):
    c = choices.get(difficulty, {}).get(player, rand)()
    result = player+c[0]
    return 'Computer plays {}. {}'.format(c, results.get(result, 'Tie.'))
    
choices = {'e':{'r':lambda: 'scissors',
                's':lambda: 'paper',
                'p':lambda: 'rock'},
           'h':{'r':lambda: 'paper',
                's':lambda: 'rock',
                'p':lambda: 'scissors'}
          }
results = {'rp':'You lose!',
          'rs':'You win!',
          'pr':'You win!',
          'ps':'You lose!',
          'sr':'You lose!',
          'sp':'You win!',
         }
difficulty = 'e'

if __name__ == '__main__':
    while 1:
        i = input('Enter a difficulty, play, or quit: ').lower()[:1]
        if i == 'q':
            break
        if i in set('emh'):
            difficulty = i
        elif i in set('rps'):
            print(win(i, difficulty))