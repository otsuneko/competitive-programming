N = int(input())

L = [0]*(N+1)
L[0] = 2
L[1] = 1
for i in range(2,N+1):
    L[i] = L[i-1] + L[i-2]
print(L[N])