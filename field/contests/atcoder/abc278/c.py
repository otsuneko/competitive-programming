N,Q = map(int,input().split())
from collections import defaultdict
follow = defaultdict(set)
for _ in range(Q):
    T,A,B = map(int,input().split())
    A,B = A-1,B-1
    if T == 1:
        follow[A].add(B)
    elif T == 2:
        if B in follow[A]:
            follow[A].remove(B)
    elif T == 3:
        if B in follow[A] and A in follow[B]:
            print("Yes")
        else:
            print("No")