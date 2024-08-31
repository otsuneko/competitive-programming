import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

ans = 0
while 1:
    ans += 1
    A.sort(reverse=True)
    A[0] -= 1
    A[1] -= 1

    cnt = 0
    for i in range(N):
        if A[i] > 0:
            cnt += 1
    if cnt <= 1:
        break
print(ans)
