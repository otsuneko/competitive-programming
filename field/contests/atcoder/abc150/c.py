N =int(input())
P =tuple(map(int,input().split()))
Q =tuple(map(int,input().split()))

import itertools

a = b = 0
for i,ptr in enumerate(itertools.permutations([i+1 for i in range(N)])):
    if ptr == P:
        a = i+1
    if ptr == Q:
        b = i+1

print(abs(a-b))