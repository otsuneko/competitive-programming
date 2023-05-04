S = list(input())
S = S[::-1]

ans = 0
from collections import defaultdict
dict = defaultdict(int)

cur = 0
dict[cur] += 1
for i,s in enumerate(S):
    cur = (int(s)*pow(10,i,2019) + cur)%2019
    if dict[cur]:
        ans += dict[cur]
    dict[cur] += 1
print(ans)