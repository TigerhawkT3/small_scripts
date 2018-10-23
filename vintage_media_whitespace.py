expression = [None for shapes in[{
'cassette':[' ______________ ',
            '|   __    __   |',
            '|  /  \  /  \  |',
            '|  \__/  \__/  |',
            '|  __________  |',
            '|_/_O______O_\_|'],
'vhs':[' ______________________  ',
       '|                      | ',
       '|     ____________     | ',
       '|    /  |      |  \    | ',
       '|   |   |      |   |   | ',
       '|    \__|______|__/    | ',
       '||____________________|| ',
       '|______________________| '],
'floppy':[' _____________   ',
          '||   |    _ |  | ',
          '||   |   | ||  | ',
          '||   |   |_||  | ',
          '||___|______|  | ',
          '| ___________  | ',
          '||           | | ',
          '||           | | ',
          '||           | | ',
          '||___________|_| '],
'snes':['    _____________     ',
        ' __||           ||__  ',
        '|__||           ||__| ',
        '|__||___________||__| ',
        '|__| ___________ |__| ',
        '|__||           ||__| ',
        '|__||___________||__| ']}]
for rows, columns, shape, square, upper, left in
((*map(int, rc), shapes[s], o not in ('ul', 'ur', 'll', 'lr'), o[0] == 'u', o[1:2] == 'l')
    for *rc, s, o in map(str.split, map(str.lower, iter(lambda: input('''\
Enter rows, columns, shape (cassette, VHS, floppy, SNES),
and orientation (square, UR, UL, LR, LL) separated by space,
or leave blank to exit:\n'''), ''))))
    for row in range(rows)
        for line in shape if
            print(
                line*columns
            if square
            else
                f'{line*min(columns, rows*upper + ((-1)**upper)*row + (not upper)):{"><"[left]}{len(line)*columns}}')]