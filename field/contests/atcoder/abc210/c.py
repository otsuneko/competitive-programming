from collections import defaultdict
dict = defaultdict(int)
N,K = map(int,input().split())
C = list(map(int,input().split()))

tmp_ans = 0
for i in range(K):
    if dict[C[i]] == 0:
        tmp_ans += 1
    dict[C[i]] += 1

ans = tmp_ans
for i in range(1,N-K+1):
    if dict[C[i-1]] == 1:
        tmp_ans -= 1
    dict[C[i-1]] -= 1
    if dict[C[i+K-1]] == 0:
        tmp_ans += 1
    dict[C[i+K-1]] += 1
    ans = max(tmp_ans,ans)

print(ans)
