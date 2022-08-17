from collections import defaultdict
N = int(input())
D = list(map(int,input().split()))
mod = 998244353

dict = defaultdict(list)
for i,d in enumerate(D):
    dict[d].append(i)
ma = max(D)

if D[0] != 0:
    print(0)
    exit()

if len(dict[0]) != 1:
    print(0)
    exit()

for i in range(1,ma+1):
    if len(dict[i]) == 0:
        print(0)
        exit()

ans = 1
for i in range(1,ma+1):
    ans = ans * pow(len(dict[i-1]),len(dict[i]),mod) % mod

print(ans)