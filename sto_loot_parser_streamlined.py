import re
import datetime
import time
import sys
import collections
import os
import pickle
import tzlocal

now = tzlocal.get_localzone().localize(datetime.datetime.now())
min_date = tzlocal.get_localzone().localize(datetime.datetime(2002, 1, 1))

class Loot:
    def __init__(self, d, t, interaction, winner, quantity, item):

        #self.datetime = tzlocal.get_localzone().localize(datetime.datetime.strptime(d+t, '%Y%m%d%H%M%S'))
        self.datetime = tzlocal.get_localzone().localize(datetime.datetime(year=int(d[:4]), month=int(d[4:6]),
            day=int(d[6:]), hour=int(t[:2]), minute=int(t[2:4]), second=int(t[4:])))
        
        quantity = quantity or ''
        quantity = (int(quantity.strip().replace(',','') or 0) or
                         int(''.join(item.split(' x ')[1:]).replace(',','') or 1))
        
        item = item.split(' x ')[0].rstrip('!.').rsplit(' erhalten', maxsplit=1)[0]
        
        self.interaction = interaction or ''
        
        if interaction in {'lost', 'placed a bet of', 'discarded', 'spent'}:
            self.gain_item = ''
            self.gain_value = 0
            self.loss_item = item
            self.loss_value = quantity * -1
        elif interaction == 'sold':
            item, gain = item.rsplit(' for ', maxsplit=1)
            self.loss_item = item
            self.loss_value = -1
            quantity, item = gain.split(maxsplit=1)
            self.gain_item = item
            self.gain_value = int(quantity.replace(',', ''))
        elif interaction == "didn't win any":
            self.gain_item = item
            self.gain_value = 0
            self.loss_item = ''
            self.loss_value = 0
        else:
            self.gain_item = item
            self.gain_value = quantity
            self.loss_item = ''
            self.loss_value = 0

expression = (r'^\[\d+,(\d+)T(\d+),0,[^@]+@,@,,,System\]'
              r"(?:You (didn't win any|spent|discarded|lost|refined"
              r"|received|sold|placed a bet of|won)|Items? acquired:|(.*) "
              r'(?:has acquired an?|hat eine?n?))'
              r' ([0-9,]+ )?(.*)'
                )
keys = ['Contraband', 'Dilithium', 'Dilithium Ore', 'Energy Credits']
dct = {key:0 for key in keys}
day = min_date
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
                match = re.match(expression, line)
                if match:
                    loot = Loot(*match.groups())
                    loot.datetime -= loot.datetime.utcoffset()
                    if loot.datetime.day != day.day and day != min_date:
                        #print(loot.datetime.day, day.day, day, min_date)
                        print('{}-{}-{}'.format(day.year,
                                                day.month,
                                                day.day),
                              *(dct[k] for k in keys), sep='\t')
                        dct = {key:0 for key in keys}
                    day = loot.datetime
                    if loot.gain_item in dct:
                        dct[loot.gain_item] += loot.gain_value
                    if loot.loss_item in dct:
                        dct[loot.loss_item] += loot.loss_value

print('{}-{}-{}'.format(loot.datetime.year,
                        loot.datetime.month,
                        loot.datetime.day),
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
