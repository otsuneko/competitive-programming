N,M,T = map(int,input().split())
A = list(map(int,input().split()))
bonus = {}
for _ in range(M):
    x,y = map(int,input().split())
    bonus[x-1] = y

for i in range(N-1):
    if T-A[i] <= 0:
        print("No")
        exit()
    T -= A[i]
    if i+1 in bonus:
        T += bonus[i+1]
print("Yes")