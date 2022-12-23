from collections import deque
N = int(input())
A = list(map(int,input().split()))
A.sort()
A = deque(A)
A2 = []

ma = 0
cnt = 1
clr = 0
for i in range(N):
    if A[i] == cnt:
        A2.append(cnt)
        clr += 1
        cnt += 1
        ma = cnt
    else:
        break

for _ in range(clr):
    A.popleft()

while A:
    A.pop()
    if A:
        A.pop()
        if A2:
            ma = A2[-1]+1
            A2.append(ma)
        else:
            ma = 1
            A2.append(ma)
    else:
        break

print(ma)