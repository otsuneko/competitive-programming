N,Q =map(int,input().split())
A =list(map(int,input().split()))

from collections import defaultdict
pos = defaultdict(list)
for i in range(N):
    pos[A[i]].append(i+1)

for _ in range(Q):
    x,k =map(int,input().split())
    
    if len(pos[x]) < k:
        print(-1)
    else:
        print(pos[x][k-1])