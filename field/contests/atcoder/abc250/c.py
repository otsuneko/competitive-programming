from collections import defaultdict
dict = defaultdict(int)

N,Q =map(int,input().split())

for i in range(N):
    dict[i+1] = i

A = [i+1 for i in range(N)]

for _ in range(Q):
    x =int(input())
    idx = dict[x]
    if idx == N-1:
        dict[x] -= 1
        dict[A[idx-1]] += 1
        A[idx-1],A[idx] = A[idx],A[idx-1]
    else:
        dict[A[idx]] += 1
        dict[A[idx+1]] -= 1
        A[idx],A[idx+1] = A[idx+1],A[idx]

print(*A)