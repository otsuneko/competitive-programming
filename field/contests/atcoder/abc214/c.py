N = int(input())
S = list(map(int,input().split()))
T = list(map(int,input().split()))

snuke = [10**18]*N
for i in range(N*2):
    snuke[i%N] = min(T[i%N],snuke[(i-1)%N]+S[(i-1)%N])

for s in snuke:
    print(s)