import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

def dfs(ans,p,idx):
    if idx == N:
        # print(*ans, sep="\n")
        # 全ての行にABCがいるか
        for y in range(N):
            if not ("A" in ans[y] and "B" in ans[y] and "C" in ans[y]):
                return

        # 全ての列にABCがいるか
        inv = list(zip(*ans))
        for y in range(N):
            if not ("A" in inv[y] and "B" in inv[y] and "C" in inv[y]):
                return

        # i 列目に書かれた文字の中で最も上にある文字は C の i 文字目と一致するか
        for y in range(N):
            for x in range(N):
                if inv[y][x] == ".":
                    continue
                if inv[y][x] != C[y]:
                    return
                else:
                    break

        print("Yes")
        for y in range(N):
            print("".join(ans[y]))
        exit()

    li = [i for i in range(p[idx]+1,N)]
    for cmb in itertools.combinations(li,2):
        second,third = cmb
        if R[idx] == "A":
            ans[idx][second] = "B"
            ans[idx][third] = "C"
            dfs(ans,p,idx+1)
            ans[idx][second] = "C"
            ans[idx][third] = "B"
            dfs(ans,p,idx+1)
            ans[idx][second] = "."
            ans[idx][third] = "."
        elif R[idx] == "B":
            ans[idx][second] = "A"
            ans[idx][third] = "C"
            dfs(ans,p,idx+1)
            ans[idx][second] = "C"
            ans[idx][third] = "A"
            dfs(ans,p,idx+1)
            ans[idx][second] = "."
            ans[idx][third] = "."
        elif R[idx] == "C":
            ans[idx][second] = "B"
            ans[idx][third] = "A"
            dfs(ans,p,idx+1)
            ans[idx][second] = "A"
            ans[idx][third] = "B"
            dfs(ans,p,idx+1)
            ans[idx][second] = "."
            ans[idx][third] = "."

N = int(input())
R = input()
C = input()

l = [0,1,2]
if N == 3:
    l = [0]
elif N == 4:
    l = [0,1]
elif N == 5:
    l = [0,1,2]

import itertools

for prod in itertools.product(l, repeat=N):
    ans = [["."]*N for _ in range(N)]
    for y,p in enumerate(prod):
        ans[y][p] = R[y]

    dfs(ans,prod,0)

print("No")