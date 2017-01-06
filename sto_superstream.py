import datetime
import sys
import os
import tzlocal

min_date = tzlocal.get_localzone().localize(datetime.datetime(2002, 1, 1))
min_date -= min_date.utcoffset()
day = min_date
keys = ['Contraband', 'Dilithium', 'Dilithium Ore', 'Energy Credits']
dct = {key:0 for key in keys}
files = sorted(f for f in os.listdir() if f[:5]=="Chat_")
l = len(files)
try:
    with open('lastlog.txt') as f:
        lastlog = f.read()
except (FileNotFoundError, PermissionError):
    lastlog = ''

print('Date', *keys, sep='\t')
for counter,fname in enumerate(files):
    if fname >= lastlog:
        print('Processing {} out of {}...'.format(counter, l), end='\r', file=sys.stderr)
        with open(fname, encoding='utf-8-sig') as f:
            for line in f:
                if (line[26:70] == ",0,NumericReceived@,@,,,System]You received " and
                    ('Dilithium' in line or 'Energy Credits' in line)):
                    quantity,item = line.strip()[70:].split(None, 1)
                    quantity = int(quantity.replace(',', ''))
                    if item == 'Refined Dilithium':
                        item = 'Dilithium'
                elif line[26:66] == ",0,NumericReceived@,@,,,System]You sold ":
                    item = 'Energy Credits'
                    quantity = int(line.rsplit(None, 3)[1].replace(',', ''))
                elif line[26:78] == ",0,NumericConversionSuccess@,@,,,System]You refined ":
                    item = 'Dilithium'
                    quantity = int(line[78:-11].replace(',', ''))
                elif (line[26:56] == ",0,NumericLost@,@,,,System]You" and
                        (line[56:62] == " lost " or line[56:63] == " spent ") and 
                      ('Dilithium' in line or 'Energy Credits' in line)):
                    quantity,item = line[62:].strip().split(None, 1)
                    quantity = -int(quantity.replace(',', ''))
                    if item == 'Refined Dilithium':
                        item = 'Dilithium'
                elif line[26:83] == ',0,ItemReceived@,@,,,System]Items acquired: Contraband x ':
                    quantity = int(line[70:].rsplit(None, 1)[1].replace(',', ''))
                    item = 'Contraband'
                elif line[26:79] == ",0,ItemReceived@,@,,,System]Item acquired: Contraband":
                    quantity = 1
                    item = 'Contraband'
                else:
                    continue
                dt = tzlocal.get_localzone().localize(datetime.datetime(year=int(line[11:15]), month=int(line[15:17]),
                     day=int(line[17:19]), hour=int(line[20:22]), minute=int(line[22:24]), second=int(line[24:25])))
                dt -= dt.utcoffset()
                if dt.day != day.day and day != min_date:
                    print('{}-{}-{}'.format(day.year,
                                            day.month,
                                            day.day),
                          *(dct[k] for k in keys), sep='\t')
                    dct = {key:0 for key in keys}
                day = dt
                if item in dct:
                    dct[item] += quantity

print('{}-{}-{}'.format(dt.year,
                        dt.month,
                        dt.day),
      *(dct[k] for k in keys), sep='\t')

print('\nDone.', file=sys.stderr)

last = files[-1][5:15]
current = files[-1]
for fname in files[::-1]:
    current = fname
    if fname[5:15] != last:
        break

with open('lastlog.txt', 'w') as f:
    f.write(current)
