A,B,C = map(int,input().split())

if A%2 or B%2 or C%2:
    print(0)
    exit()

if A == B == C:
    print(-1)
    exit()

ans = 0
while A%2 == 0 and B%2 == 0 and C%2 == 0:
    A,B,C = B//2+C//2, A//2+C//2, A//2+B//2
    ans += 1
print(ans)