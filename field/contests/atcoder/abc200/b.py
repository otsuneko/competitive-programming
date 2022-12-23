N,K = map(int,input().split())

for i in range(K):
    if N%200:
        N = int(str(N)+"200")
    else:
        N = N//200
print(N)