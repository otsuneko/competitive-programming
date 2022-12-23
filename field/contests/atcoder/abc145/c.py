def nPr(n, k):
    fact = [0 for _ in range(n + 1)]
 
    # base case
    fact[0] = 1
 
    # Calculate value
    # factorials up to n
    for i in range(1, n + 1):
        fact[i] = i * fact[i - 1]
 
    # P(n, k) = n!/(n-k)!
    return fact[n] // fact[n - k]

N =int(input())
pos =[list(map(int,input().split())) for _ in range(N)]

l = 0

import itertools

for ptr in itertools.permutations([i for i in range(N)], N):
    for i in range(N-1):
        y1,x1 = pos[ptr[i]]
        y2,x2 = pos[ptr[i+1]]
        l += ((y2-y1)**2 + (x2-x1)**2)**0.5

print(l/nPr(N,N))
