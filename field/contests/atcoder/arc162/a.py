import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

T = int(input())

for _ in range(T):
    N = int(input())
    P = list(map(int,input().split()))

    ans = N
    flg = False
    for i in range(N):
        if P[i] > i+1:
            ans -= 1
            flg = True
        elif P[i] == i+1 and flg:
            ans -= 1

    print(ans)
