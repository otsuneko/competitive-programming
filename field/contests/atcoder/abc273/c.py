N = int(input())
A = list(map(int,input().split()))

A2 = list(set(A))
A2.sort()

from collections import Counter
count = Counter(A)

for k in range(N):
    if len(A2)-k-1 >= 0:
        print(count[A2[len(A2)-k-1]])
    else:
        print(0)