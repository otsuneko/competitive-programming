N = int(input())
S = list(input())
Q = int(input())

flg = False
for _ in range(Q):
    t,a,b = map(int,input().split())
    a -= 1
    b -= 1

    if t == 1:
        if flg:
            a = (a+N)%(2*N)
            b = (b+N)%(2*N)
        S[a],S[b] = S[b],S[a]
    else:
        flg = not flg

if flg:
    S = S[N:] + S[:N]
print("".join(S))
