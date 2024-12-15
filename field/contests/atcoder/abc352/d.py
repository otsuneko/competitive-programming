import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
P = list(map(int,input().split()))

from collections import deque
# arr内の連続する長さKのスライディングウィンドウ中の最小値を(N-K+1)区間分求める
# arrの各要素を[-x for x in arr]と正負反転して与えれば最大値が求まる
def sliding_window_minimum(arr, K):
    ans = []
    d = deque() # dequeは常に単調増加になるよう管理
    for i in range(len(arr)):
        # 新入りがdequeの末尾(最大値)になれるように新入り以上の要素を削除
        while d and arr[i] <= arr[d[-1]]:
            d.pop()
        # 新入りを末尾(最大値)に追加
        d.append(i)
        # SWの長さがK以上ならd[0]がその時点の最小値
        if i >= K-1:
            ans.append(arr[d[0]])
        # d[0]がSWの先頭idx(i+1-K)以下ならSW範囲外として削除しておく
        if d and d[0] <= i+1-K:
            d.popleft()
    return ans

idxs = [-1]*N
for i in range(N):
    idxs[P[i]-1] = i
MI = sliding_window_minimum(idxs,K)
MA = sliding_window_minimum([-x for x in idxs],K)

ans = INF
for ma,mi in zip(MA,MI):
    ans = min(ans, -ma-mi)
print(ans)
