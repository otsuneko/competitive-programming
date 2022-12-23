N = int(input())
P = list(map(int,input().split()))

idx = 0
for i in range(N-1):
    if P[i] > P[i+1]:
        idx = i

for i in range(N-1,0,-1):
    if P[idx] > P[i]:
        P[idx],P[i] = P[i],P[idx]
        break

print(*P[:idx+1],*P[idx+1:][::-1])