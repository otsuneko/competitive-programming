import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T =  map(int,input().split())
change = []
for _ in range(T):
    a,b =  map(int,input().split())
    change.append((a-1,b))

score = [0]*N
s = set([0])
from collections import Counter
count = Counter(score)


for a,b in change:
    count[score[a]] -= 1
    if count[score[a]] == 0:
        s.remove(score[a])
    score[a] += b
    if count[score[a]] == 0:
        s.add(score[a])
    count[score[a]] += 1
    print(len(s))
