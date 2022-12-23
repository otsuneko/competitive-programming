N,L,K = map(int,input().split())
for _ in range(N):
    S = input()

def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

print(nCr(1000,10))