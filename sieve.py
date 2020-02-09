def sieve(m):
    '''returns a list of all primes from 2 to m'''
    m += 1
    L = list(range(m)) # create the list
    L[1] = 0 # 0 and 1 are non-prime, so mark 1
    p = 2 # initialize to 2
    while p < m:
        for i in range(p**2, m, p): # find multiples
            L[i] = 0 # mark them
        for i in range(p+1, m): # find the next p
            if L[i]:
                p = L[i] # set the new p
                break
        else:
            break # no more new primes, so done
    return list(filter(None, L)) # return ummarked nums