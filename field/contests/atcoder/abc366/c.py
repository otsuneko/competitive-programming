import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

Q = int(input())
from collections import defaultdict
dic = defaultdict(int)
s = set()
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]
        dic[x] += 1
        s.add(x)
    elif query[0] == 2:
        x = query[1]
        dic[x] -= 1
        if dic[x] == 0:
            s.remove(x)
    else:
        print(len(s))
