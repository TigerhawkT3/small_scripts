def recursive_compute(n, k, p, d=None): # total 2**k calls
    p[0] += 1
    return int(n in (1, k)) or recursive_compute(n-1, k-1, p) + recursive_compute(n, k-1, p)
    
def recursive_memoize(n, k, p, d): # total k**1.1 calls
    p[0] += 1
    if n in (1, k):
        return 1
    if (n-1,k-1) not in d:
        d[(n-1,k-1)] = recursive_memoize(n-1,k-1, p, d)
    if (n,k-1) not in d:
        d[(n,k-1)] = recursive_memoize(n,k-1, p, d)
    return d[(n-1,k-1)] + d[(n,k-1)]
    
def triangle(rows, f, c, d=None):
    # number of rows, function (recursive_compute or recursive_memoize),
    # counter (p1 or p2), dictionary (dct)
    for k in range(1, rows+1):
        print(' '.join(f'{f(n,k,c,d):03d}' for n in range(1, k+1)).center(4*rows-1))
    print(c[0])

def iterative(rows):
    if rows<4:
        pad = 1
    else:
        n = 2
        for i in range(1, rows-2):
            if i%2:
                n += n * (i//2+1) // (i//2+2)
            else:
                n *= 2
        pad = len(str(n))
    print(f'{"0"*(pad-1)}1'.center((pad+2)*(rows-2)+2))
    if rows == 1: return print()
    print(f'{"0"*(pad-1)}1 {"0"*(pad-1)}1'.center((pad+2)*(rows-2)+2))
    if rows == 2: return print()
    print(f'{"0"*(pad-1)}1 {"0"*(pad-1)}2 {"0"*(pad-1)}1'.center((pad+2)*(rows-2)+2))
    if rows == 3: return print()
    row = 1, 2, 1
    for _ in range(rows-3):
        row = (1, *(row[i] + row[i+1] for i in range(len(row)-1)), 1)
        print(' '.join(f'{n:0{pad}d}' for n in row).center((pad+2)*(rows-2)+1))
    
    print()

if __name__ == '__main__':
    dct = {} # dictionary for recursive_memoize
    p1 = [0] # number of calls for recursive_compute
    p2 = [0] # number of calls for recursive_memoize
    triangle(10, recursive_compute, p1)
    triangle(10, recursive_memoize, p2, dct)
    iterative(20)