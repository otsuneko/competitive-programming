N = int(input())
S = list(input())
Q = int(input())

flag = False
for i in range(Q):
    t,a,b = map(int,input().split())
    a -= 1
    b -= 1

    if t == 1:
        if flag:
            a += N
            b += N
            a %= (2*N)
            b %= (2*N)
        S[a],S[b] = S[b],S[a]
    elif t == 2:
        flag = not flag

if flag:
    S = S[N:]+S[:N]

print("".join(S))