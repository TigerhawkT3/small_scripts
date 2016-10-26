import sys
import random
import time

def fours(name, hand): # checks a name/hand for wins
    for card in set(hand):
        if hand.count(card) == 4:
            for i in range(4):
                hands[name].remove(card)
            scores[name] += 1
            print('{} cleared the {}!'.format(name, card))

deck = list('0123456789JQK'*4)
random.shuffle(deck)
    
scores = {name:0 for name in (sys.argv[1:] if sys.argv[2:] else list('1234'))}
names = list(scores)

if len(scores) > 4:
    hand_size = 5
else:
    hand_size = 7

hands = {name:[deck.pop() for i in range(hand_size)] for name in scores}

for name,hand in hands.items():
    fours(name, hand)

idx = 0
while 1:
    player = names[idx]
    if not hands[player]: # handles player not having a hand
        if deck:
            hands[player].append(deck.pop())
        else:
            idx += 1
            if idx >= len(names):
                idx = 0
            continue
            
    if player.startswith('AI_'):
        ask = random.choice([name for name in names if name != player])
        card = random.choice(hands[player])
        print('{} asks for {} from {}.'.format(player, card, ask))
    else:
        while 1: # handles input and viewing your hand
            inp = input('{}\'s turn. Name and card? '.format(player))
            if inp:
                try:
                    ask, card = inp.split()
                except ValueError:
                    print('Enter a name and card, separated by spaces.')
                else:
                    card = card.upper()
                    if card in hands[player] and ask != player and ask in scores:
                        break
                    else:
                        print('Name must belong to a player other than yourself, and you must have the card.')
            else:
                print('Printing {}\'s hand for 5 seconds in 5 seconds.'.format(player))
                time.sleep(5)
                print(*sorted(hands[player]), sep='', end='\r', flush=True)
                time.sleep(5)
                print(' '*len(hands[player]), end='\r', flush=True)
                
    success = False
    while card in hands[ask]:
        hands[ask].remove(card)
        hands[player].append(card)
        success = True
    if not success:
        if deck:
            print('Go fish!')
            hands[player].append(deck.pop())
            if hands[player][-1] == card:
                success = True
                print('Fished the {}! Lucky!'.format(card))
        else:
            print('Can\'t fish - no deck.')
    else:
        print('{} got the {} from {}.'.format(player, card, ask))
    if not success:
        idx += 1
        if idx >= len(names):
            idx = 0
            
    fours(player, hands[player])
            
    if sum(scores.values()) == 13:
        print('Scores:')
        size = max(map(len, names))
        for k in sorted(scores, key=scores.get, reverse=True):
            print(k.ljust(size), scores[k])
        break