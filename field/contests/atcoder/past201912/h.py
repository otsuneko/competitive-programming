N = int(input())
C = list(map(int,input().split()))
Q = int(input())

ans = 0
min_odd = 10**18
for i in range(0,N,2):
    min_odd = min(min_odd, C[i])
min_all = min(C)
minus_odd = minus_all = 0
for _ in range(Q):
    S = list(map(int,input().split()))
    if S[0] == 1:
        x,a = S[1]-1, S[2]
        minus = a + minus_odd + minus_all if x%2 == 0 else a + minus_all
        if C[x] >= minus:
            ans += a
            C[x] -= a
            if x%2 == 0:
                min_odd = min(min_odd, C[x])
            min_all = min(min_all, C[x])
    elif S[0] == 2:
        a = S[1]
        if min_odd >= a + minus_odd + minus_all:
            ans += a*(N+1)//2
            min_odd -= a
            min_all 
            minus_odd += a
    elif S[0] == 3:
        a = S[1]
        if min_all >= a + minus_all:
            ans += a*N
            min_odd -= a
            min_all -= a
            minus_all += a

print(ans)