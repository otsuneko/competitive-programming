N,K = map(int,input().split())
T = list(input())

for i in range(N):
    if i >= K-1:
        T[i] = T[i].swapcase()
print("".join(T))