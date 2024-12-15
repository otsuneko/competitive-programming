import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())

check = set()

for _ in range(M):
    a,b = map(str,input().split())
    a = int(a)-1

    if b == "M":
        if a not in check:
            print("Yes")
            check.add(a)
            continue
    print("No")
