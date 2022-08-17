N = int(input())
A = list(map(int,input().split()))
Q = int(input())

from collections import Counter
count = Counter(A)
total = sum(A)

for _ in range(Q):
    B,C = map(int,input().split())
    
    if count[B]:
        total += (C-B) * count[B]
        count[C] += count[B]
        count[B] = 0
    
    print(total)