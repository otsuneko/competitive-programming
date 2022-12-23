from collections import defaultdict

N = int(input())
A = list(map(int,input().split()))
base = -1
add = defaultdict(int)

Q = int(input())
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]
        base = x
        add = defaultdict(int)
    elif query[0] == 2:
        i,x = query[1:]
        add[i-1] += x
    elif query[0] == 3:
        i = query[1]
        if base > -1:
            print(base + add[i-1])
        else:
            print(A[i-1] + add[i-1])