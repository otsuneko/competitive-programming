S = list(input())

from collections import defaultdict
dict = defaultdict(int)

for a in S:
    dict[a] += 1

even = 0
for key in dict:
    even += dict[key]//2

ans = 0
for i in range(1,even+1):
    ans += len(S)-i-2*(i-1)

print(ans)