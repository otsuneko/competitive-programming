N = int(input())
from collections import defaultdict
dict = defaultdict(int)

ans = 0
for _ in range(N):
    s = list(input())
    s.sort()
    s2 = "".join(s)
    ans += dict[s2]
    dict[s2] += 1
print(ans)