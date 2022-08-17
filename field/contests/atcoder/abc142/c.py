N = int(input())
A = list(map(int,input().split()))

rec = []
for i in range(N):
    rec.append((A[i],i))

rec.sort()

ans = []
for r in rec:
    ans.append(r[1]+1)
print(*ans)