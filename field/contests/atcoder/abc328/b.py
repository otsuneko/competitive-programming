import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
D = list(map(int,input().split()))

ans = 0
for m,dd in enumerate(D):
    m += 1
    for d in range(dd):
        d += 1
        li = set(list(str(m)) + list(str(d)))
        if len(li) == 1:
            ans += 1
print(ans)