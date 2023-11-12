import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()
ans = []
for s in S:
    if s in ["A","B"]:
        ans.append(s)
    else:
        if len(ans) >= 2 and ans[-2:] == ["A","B"]:
            ans.pop()
            ans.pop()
        else:
            ans.append(s)

print("".join(ans))