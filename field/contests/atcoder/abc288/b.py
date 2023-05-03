N,K = map(int,input().split())
S = [input() for _ in range(N)]

ans = S[:K]
ans.sort()
for a in ans:
    print(a)