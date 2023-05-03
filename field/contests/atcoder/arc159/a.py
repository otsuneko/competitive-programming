N,K = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(N)]
INF =10**18

Q = int(input())
for _ in range(Q):
    s,t = map(int,input().split())
    s,t = s-1,t-1

    start = set([s%N])
    for i in range(100):
        for c in list(start):
            if A[c][t%N] == 1:
                print(i+1)
                break
            else:
                for j in range(N):
                    if A[c][j] == 1:
                        start.add(j)
        else:
            continue
        break
    else:
        print(-1)