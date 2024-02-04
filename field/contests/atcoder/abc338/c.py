import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
Q = list(map(int,input().split()))
A = list(map(int,input().split()))
B = list(map(int,input().split()))

#Aが最大何皿作れるか
maxA = INF
for i in range(N):
    if A[i] == 0:
        continue
    maxA = min(maxA, Q[i]//A[i])

#Aが1皿減るごとにBが何皿増やせるか
remain = [0]*N
for i in range(N):
    if B[i] == 0:
        continue
    remain[i] = Q[i] - A[i]*maxA

curB = INF
for i in range(N):
    if B[i] == 0:
        continue
    curB = min(curB, remain[i]//B[i])

ans = maxA+curB
for i in range(1,maxA+1):
    curB = INF
    for j in range(N):
        remain[j] += A[j]
        if B[j] > 0:
            curB = min(curB, remain[j]//B[j])
    ans = max(ans, maxA-i+curB)
print(ans)