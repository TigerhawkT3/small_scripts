items = {'cassette':[' ______________ ',
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
                 '|__||___________||__| ']}
while 1:
    i = input('''Enter rows, columns, shape (cassette, VHS, floppy, SNES),
and orientation (square, UR, UL, LR, LL) separated by space,
or leave blank to exit:\n''')
    if not i:
        break
    rows, columns, shape, orientation = i.split()
    rows = int(rows)
    columns = int(columns)
    shape = items[shape.lower()]
    square = orientation.lower() not in ('ul', 'ur', 'll', 'lr')
    upper = orientation[0].lower() == 'u'
    left = orientation[1:2].lower() == 'l'
    for row in range(rows):
        for line in shape:
            if square:
                print(line*columns)
            else:
                content = line * min(columns, rows*upper + ((-1)**upper)*row + (not upper))
                if not left:
                    content = content.rjust(len(line)*columns)
                print(content)