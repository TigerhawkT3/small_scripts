while 1:
    num = input('Number? ')
    try:
        num = int(num)
    except ValueError:
        print('Must be a number.')
        continue
    if num < 3:
        print('too low')
    elif num > 3:
        print('too high')
    else:
        print('correct')
        break