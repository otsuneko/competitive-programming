import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
import math
T = int(input())
for _ in range(T):
    N,X,K = map(int,input().split())

    max_depth = math.floor(math.log2(N))
    cur_depth = math.floor(math.log2(X))
    # print(max_depth,cur_depth)

    ans = 0
    # 下にK移動したとき最大の深さを越えない
    if cur_depth + K <= max_depth:
        print("1")
        left = X * 2**(max(0,cur_depth + K - 1))
        right = left + 2 ** (max(0,cur_depth + K - 2))
        print(left,right)
        if N >= left:
            ans += min(N,right) - left + 1
        if K == 0:
            print(ans)
            continue

    # 上にK移動した時根にちょうど辿り着くor辿り着かない
    if cur_depth >= K:
        print("2")
        ans += 2**(max(0,cur_depth - K - 1))
    # 上にK移動した時根を超えてかつ最大の深さを超えない
    elif K <= cur_depth + max_depth:
        print("3")
        if X%2:
            left = X * 2**(max(0,K - cur_depth - 1))
            right = left + 2 ** (max(0,K - cur_depth - 2))
        else:
            left = (X+1) * 2**(max(0,K - cur_depth - 1))
            right = left + 2 ** (max(0,K - cur_depth - 2))

        if N >= left:
            ans += min(N,right) - left + 1
        ans += 2**(max(0,K - cur_depth - 1))

    print(ans)