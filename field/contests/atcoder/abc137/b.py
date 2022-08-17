K,X = map(int,input().split())

ans = []
for i in range(max(-1000000, X-K+1), min(1000000, X+K)):
    ans.append(i)
print(*ans)