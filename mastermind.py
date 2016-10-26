import random
import collections

length = 4
guesses = 12
pattern = [random.choice('abcdef') for _ in range(length)]
counted = collections.Counter(pattern)

def running():
    guess = input('?: ')
    guess_count = collections.Counter(guess)
    close = sum(min(counted[k], guess_count[k]) for k in counted)
    exact = sum(a==b for a,b in zip(pattern, guess))
    close -= exact
    print('Exact: {}. Close: {}.'.format(exact, close))
    return exact != length

for attempt in range(guesses):
    if not running():
        print('Done!')
        break
    else:
        print('Guesses remaining:', guesses - 1 - attempt)
else:
    print('Game over. The code was {}.'.format(''.join(pattern)))