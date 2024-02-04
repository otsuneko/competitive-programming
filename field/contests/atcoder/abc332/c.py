import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = input()

ans = 0
logot = 0
mujit = M
for s in S:
    if s == "0":
        logot = ans
        mujit = M
    elif s == "1":
        if mujit > 0:
            mujit -= 1
        elif logot > 0:
            logot -= 1
        else:
            ans += 1
    elif s == "2":
        if logot == 0:
            ans += 1
        else:
            logot -= 1

    # print(logot,mujit,ans)
print(ans)