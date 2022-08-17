N =int(input())
A =list(map(int,input().split()))
A2 = []
for i in range(N):
    A2.append(A[i]-(i+1))
A2.sort()
med = A2[N//2]

ans = 0
for i in range(N):
    ans += abs(A[i]-(med+i+1))
print(ans)