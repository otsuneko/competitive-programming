N = int(input())
A = list(map(int,input().split()))
from collections import Counter
count = Counter(A)

ans = 0
seen = set()
for key in count:
    for key2 in count:
        ans += count[key]*count[key2]*(key-key2)**2
print(ans//2)
