from collections import defaultdict
dict = defaultdict(int)

N = int(input())
for _ in range(N):
    dict[input()] += 1

ans = ""
ma = 0
for key in dict:
    if dict[key] > ma:
        ma = dict[key]
        ans = key
print(ans)