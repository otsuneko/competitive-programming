N = int(input())
S = input()
MOD = 998244353

from collections import defaultdict
dp = defaultdict(int)
dp[tuple([0]*10)] = 1

for i in range(N):
    ndp = defaultdict(int)
    for key,val in dp.items():
        print(key,val)
        li = list(key)
        idx = ord(S[i])-ord("A")
        if li[idx] > 0 and sum(li) != li[idx]:
            continue
        li[idx] += 1
        ndp[tuple(li)] += val
        ndp[tuple(li)] %= MOD
    dp = ndp

ans = 0
for key,val in dp.items():
    ans += val
    ans %= MOD
print(ans)
