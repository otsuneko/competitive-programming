N = int(input())
A = list(map(int,input().split()))
MOD = 10**9+7

from collections import defaultdict
dict = defaultdict(list)
for i in range(N):
    dict[A[i]].append(i)

# print(dict)

ans = 1
for key in dict:
    if key == 0 and len(dict[key]) != 1:
        ans = 0
        break
    elif key != 0 and len(dict[key]) != 2:
        ans = 0
        break
    else:
        ans = ans * len(dict[key]) % MOD

print(ans)