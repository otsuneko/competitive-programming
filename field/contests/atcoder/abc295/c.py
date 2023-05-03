from collections import defaultdict
dict = defaultdict(int)

N = int(input())
A = list(map(int,input().split()))

for a in A:
    dict[a] += 1

ans = 0
for key in dict:
    ans += dict[key]//2

print(ans)