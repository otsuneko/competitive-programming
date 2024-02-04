import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
A = list(map(int,input().split()))

# 余り無しの場合
if K%2 == 0:
    ans = 0
    for i in range(K//2):
        ans += A[2*i+1]-A[2*i]
    print(ans)
    exit()

# 余りありの場合(左右から累積和)
cumsum_l = [0]
cumsum_r = [0]
for i in range(K//2):
    cumsum_l.append(cumsum_l[-1] + A[2*i+1] - A[2*i])
    cumsum_r.append(cumsum_r[-1] + A[K-1 - 2*i] - A[K-1 - (2*i+1)])

ans = INF
for i in range(K//2+1):
    ans = min(ans, cumsum_l[i] + cumsum_r[K//2 - i])
print(ans)