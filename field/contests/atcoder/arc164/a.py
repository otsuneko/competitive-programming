import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

T = int(input())
for _ in range(T):
    N,K = map(int,input().split())

    while 1:
        m = 0
        # print(N,K)
        while 1:
            if 3**m >= N:
                break
            m += 1
        m = max(0,m-1)
        mul = N // (3**m)
        N -= (3**m) * mul
        K -= mul
        if N <= 0:
            if K == 0:
                print("Yes")
            else:
                print("No")
            break