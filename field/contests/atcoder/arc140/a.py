def divisor(n):
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]

from collections import defaultdict
N,K =map(int,input().split())
S = input()
div = divisor(N)

ans = N
for d in reversed(div):
    if d > N//2:
        continue

    li = []
    for i in range(0,N,d):
        li.append(S[i:i+d])
    
    change_cnt = 0
    for i in range(d):# i文字目
        dict = defaultdict(int)
        for s in li: # 分割文字列s
            dict[s[i]] += 1
        if len(dict) == 1: # i文字目が全て同じ
            continue
        else:
            ma = 0
            for key in dict:
                ma = max(dict[key],ma)
            change_cnt += (N//d)-ma
    if change_cnt <= K:
        ans = min(ans,d)

print(ans)