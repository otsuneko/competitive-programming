from collections import deque
N,K = map(int,input().split())
A = deque(map(int,input().split()))

for _ in range(K):
    A.popleft()
    A.append(0)
print(*A)