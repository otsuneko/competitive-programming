import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

repu = []
for i in range(1,101):
    repu.append(int("1"*i))

ans = set()
for i in range(100):
    for j in range(100):
        for k in range(100):
            ans.add(repu[i]+repu[j]+repu[k])
ans = sorted(list(ans))
print(ans[N-1])

