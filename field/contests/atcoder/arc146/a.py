N = int(input())
A = list(map(int,input().split()))

A.sort(reverse=True)

A2 = A[:3]

import itertools

ma = 0
for ptr in itertools.permutations(A2):
    ma = max(ma, int(str(ptr[0])+str(ptr[1])+str(ptr[2])))

print(ma)