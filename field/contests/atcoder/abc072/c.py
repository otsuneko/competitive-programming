from collections import defaultdict
dict = defaultdict(int)

N = int(input())
A = list(map(int,input().split()))
A2 = []
for a in A:
    dict[a-1] += 1
    dict[a] += 1
    dict[a+1] += 1

ans = 0
for key in dict:
    ans = max(ans,dict[key])
print(ans)