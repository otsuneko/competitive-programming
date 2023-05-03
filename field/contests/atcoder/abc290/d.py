T = int(input())
for _ in range(T):
    N,D,K = map(int,input().split())

    if D < N:
        if N%D == 0:
            loop = (N+D-1)//D
            div = (K-1)//loop
            mod = (K-1)%loop
            print(div + mod*D)
        else:
            loop = (N+D-1)//D
            div = (K-1)//loop
            mod = (K-1)%loop
            amari = D*loop%N
            # print(amari)
            print((div*amari)%N + mod*D)
    else:
        if D%N == 0:
            print(K-1)
        else:
            mod = D%N
            rem = N-mod
            ans = (K-1)*(-rem)%N
            print(ans)