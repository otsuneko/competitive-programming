N,Q =  map(int,input().split())
S = list(input())

last = N-1
for _ in range(Q):
    t,x = map(int,input().split())
    if t == 1:
        last = last-x
        if last < 0:
            last += N
    else:
        idx = last-N+x
        if 0<=idx<N:
            print(S[idx])
        elif idx < 0:
            print(S[idx+N])
        else:
            print(S[idx-N])