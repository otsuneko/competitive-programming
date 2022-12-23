from collections import defaultdict
N,M = map(int,input().split())
A = list(map(int,input().split()))
A.sort()

dict = defaultdict(int)
for a in A:
    dict[a] += 1

keys = sorted(dict.keys())

if len(keys) == M:
    print(0)
    exit()

ini = 0
for i in range(len(keys)):
    if keys[(i+1)%len(keys)] != (keys[i]+1)%M:
        ini = i
        break

ans = 10**18
total = sum(A)
minus = 0
cur = keys[ini]
for i in range(len(keys)):
    minus += dict[cur]*cur
    if (cur-1)%M not in dict:
        ans = min(ans, total-minus)
        minus = 0
    
    cur = keys[ini-i-1]
print(ans)