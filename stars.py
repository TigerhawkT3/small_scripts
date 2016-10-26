def triangle(shape, height, fill=' '):
    if shape == 'pyramid':
        pyramid = 2
    else:
        pyramid = 1
    lead = shape != 'left'
    print(' ' * (height+1) * lead + '*')
    for i in range(height):
        print(' ' * (height-i) * lead + (fill*(pyramid*(i+1)-1)).join('**'))
    print('*'*height*pyramid + '*'*(1+pyramid))

def rectangle(width, height, fill=' '):
    if width<2 or height<2:
        raise ValueError('Rectangle must be at least two by two.')
    print('*'*width)
    for i in range(height-2):
        print('*' + fill*(width-2) + '*')
    print('*'*width)

if __name__ == '__main__':
    rectangle(8,4, 'X')
    rectangle(4,6, '!')