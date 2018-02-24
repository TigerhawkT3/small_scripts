def rotate_array(array, angle, wide=False):
    '''
    Rotates a rectangular or diamond 2D array in increments of 45 degrees.
    Parameters:
        array (list): a list containing sliceable sequences, such as list, tuple, or str
        angle (int): a positive angle for rotation, in 45-degree increments.
        wide (bool): whether a passed diamond array should rotate into a wide array
            instead of a tall one (tall is the default). No effect on square matrices.
    '''
    angle = angle%360
    if angle < 1:
        return [list(row) for row in array]
    lengths = list(map(len, array))
    rect = len(set(lengths)) == 1
    width = max(lengths)
    height = sum(lengths)/width
    if wide:
        width, height = height, width
    if not rect:
        array = [list(row) for row in array]
        array = [[array[row+col].pop() for row in range(width)] for col in range(height)]
        angle += 45
    nineties, more = divmod(angle, 90)
    if nineties == 3:
        array = list(zip(*array))[::-1]
    else:
        for i in range(nineties):
            array = list(zip(*array[::-1]))
    if more:
        ab = abs(len(array)-len(array[0]))
        m = min(len(array), len(array[0]))
        tall = len(array) > len(array[0])
        array = [[array[r][c] for r,c in zip(range(row-1, -1, -1), range(row))
                 ] for row in range(1, m+1)
           ] + [[array[r][c] for r,c in zip(range(m-1+row*tall, row*tall-1, -1),
                                            range(row*(not tall), m+row*(not tall)+1))
                ] for row in range(1, ab+(not tall))
           ] + [[array[r][c] for r,c in zip(range(len(array)-1, ab*tall+row-1, -1),
                                            range(ab*(not tall)+row, len(array[0])+(not tall)))
                ] for row in range((not tall), m)
           ]
    return array