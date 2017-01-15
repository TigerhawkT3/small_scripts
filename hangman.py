words = {'hello', 'python'}

def user_guess(current, word):
    print('Current state:', current)
    guess = input('Letter? ')
    if guess in word and guess not in current:
        return ''.join(w if w==guess else c for c,w in zip(current, word)), word
    else:
        print('Nope! %s is not in the word.' % guess)
        return current, word

for word in words:
    current = '*'*len(word)
    remaining = 5
    while remaining:
        old_state = current
        current, word = user_guess(current, word)
        if old_state == current:
            remaining -= 1
            print('Remaining guesses: %d' % remaining)
        if current == word:
            print('You won! -', word)
            break
    else:
        print('You lost. -', word)