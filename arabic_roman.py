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
    return int(s!='NULLA') and sum((l[a], -l[a])[l[a]<l[b]] for a,b in zip(s, s[1:])) + l[s[-1]]