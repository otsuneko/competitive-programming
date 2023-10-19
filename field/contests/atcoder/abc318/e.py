import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

idx = [[] for _ in range(N+1)]
for i in range(N):
    idx[A[i]].append(i)

ans = 0
# vは端の値
for v in range(1,N+1):
    diffs = []
    # jは真ん中のindex
    for j in range(len(idx[v])-1):
        diffs.append(idx[v][j+1] - idx[v][j] - 1)
    print(diffs)

    l = len(diffs)

    for j in range(l):
        ans += diffs[j] * (l-j) * (j+1)

print(ans)










# for i in range(N):
#     A[i] -= 1

# # j = 1の時のleft[x]right[x]を求める
# left = [0]*N
# right = [0]*N
# left[A[0]] += 1
# for i in range(1,N):
#     right[A[i]] += 1
# su = 0
# for i in range(N):
#     su += left[i] * right[i]

# ans = 0
# # 真ん中固定
# for j in range(1,N-1):
#     ans += su - left[A[j]] * right[A[j]]

#     ori = left[A[j]] * right[A[j]]
#     left[A[j]] += 1
#     right[A[j]] -= 1
#     su = su - ori + left[A[j]] * right[A[j]]

# print(ans)