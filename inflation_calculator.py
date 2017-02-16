from inflation_data import *

print('Input start year and end year (1913-2016) and amount, or press Enter to quit.')

for i in iter(input, ''):
    try:
        s, e, v = i.split()
        s = int(s)
        e = int(e)
        result = float(v)
    except (TypeError, ValueError):
        print('Use e.g. "1980 2010 3.50".')
        continue
    if e > s:
        for v in data[s-min_date:e-min_date]:
            result *= v
    else:
        for v in data[s-min_date:e-min_date:-1]:
            result /= v
    print('${:.2f}'.format(result))