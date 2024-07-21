import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

minsum = 0
maxsum = 0

N = int(input())
LR = [list(map(int,input().split())) for _ in range(N)]
ans = []

for l, r in LR:
    minsum += l
    maxsum += r
    ans.append((l + r) // 2)

if not (minsum <= 0 <= maxsum):
    print("No")
    exit()

diff = sum(ans)
for i, (l,r) in enumerate(LR):
    if diff > 0:
        sub = min(diff, abs(l - ans[i]))
        ans[i] -= sub
        diff -= sub
    elif diff < 0:
        add = min(abs(diff), abs(r - ans[i]))
        ans[i] += add
        diff += add

print("Yes")
print(*ans)
