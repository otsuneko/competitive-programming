import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

ans = []
for s in S:
    ans.append(s)
    ans.append(" ")
print("".join(ans[:-1]))