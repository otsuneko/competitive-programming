K,A,B = map(int,input().split())

diff = B-A
ans = max(1 + A-1 + (K-A+1)//2*diff + (K-A+1)%2, 1+K)
print(ans)