from collections import deque
H,W = map(int,input().split())
N = int(input())
A = deque(map(int,input().split()))

ans = [0]*W

flg = False
n = 1
for h in range(H):
    for w in range(W):
        if flg:
            ans[W-1-w] = n
        else:
            ans[w] = n
        A[0] -= 1
        if A[0] == 0:
            A.popleft()
            n += 1
    flg = not flg

    print(*ans)
