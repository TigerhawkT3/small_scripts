import random

deck = list('234567890JQKA'*4)
random.shuffle(deck)
value = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
          '9':9, '0':10, 'J':10, 'Q':10, 'K':10, 'A':1}
player = [deck.pop() for _ in range(2)]
cpu = [deck.pop() for _ in range(2)]

def check(who, hand):
    subtotal = sum(map(value.get, hand))
    if subtotal > 21:
        return print('{} loses.'.format(who), *hand)
    if len(hand) > 4:
        return print('{} wins.'.format(who), *hand)
    total = [subtotal] + [item for item in 
                range(subtotal+10, subtotal+10*hand.count('A')+1, 10)
                if item <= 21]
    if 21 in total:
        return print('{} wins.'.format(who), *hand)
    return total
                    
while 1:
    pl, cp = check('Player', player), check('CPU', cpu)
    if not pl or not cp:
        break
    print(*player)
    p = input('Enter to stay. ')
    if p:
        player.append(deck.pop())
    ai = cp[-1] < 15
    if ai:
        cpu.append(deck.pop())
    if not p and not ai:
        if pl[-1] > cp[-1]:
            print('Player wins.')
        elif pl[-1] < cp[-1]:
            print('CPU wins.')
        else:
            print('Tie.')
        print('Player:', *player)
        print('CPU:', *cpu)
        break