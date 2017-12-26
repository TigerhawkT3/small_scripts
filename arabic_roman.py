def a2r(i):
    '''Takes an integer 0<=i<4000 and returns a string of its Roman numeral.'''
    n = {1: 'I', 4:'IV', 5: 'V', 9:'IX', 10: 'X', 40:'XL', 50: 'L',
         90:'XC', 100: 'C', 400:'CD', 500: 'D', 900:'CM', 1000:'M'}
    result = ''
    while i:
        num = max(x for x in n if x<=i)
        i -= num
        result += n[num]
    return result or 'nulla'

def r2a(s):
    '''Takes a Roman numeral string nulla<=s<=MMMCMXCIX and returns its integer value.'''
    s, l = s.upper(), {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    return int(s!='NULLA') and (sum((l[a], -l[a])[l[a]<l[b]] for a,b in zip(s, s[1:])) + l[s[-1]])

def roman(inp):
    '''Takes a Roman numeral string or Arabic integer and converts it to the opposite format.'''
    if isinstance(inp, int):
        if not 0<=inp<4000:
            e = f'{inp} outside acceptable range of 0 <= number < 4000.'
            raise ValueError(e)
        return a2r(inp)
    elif isinstance(inp, str):
        inp = inp.upper()
        acceptable = set('MDCLXVI')
        if inp!='NULLA' and not all(c in acceptable for c in inp):
            e = ("Roman numeral input must be 'nulla', or be less than "
                "4000 and contain only M, D, C, L, X, V, and/or I.")
            raise ValueError(e)
        return r2a(inp)
    else:
        e = ('roman() argument must be an integer or a string, not '
            f"{str(type(inp)).replace('<class ', '').rstrip('>')}.")
        raise TypeError(e)