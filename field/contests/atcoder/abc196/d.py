# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
def dfs(cur, used, A, B):
    global ans

    if cur == H*W:
        ans += 1
        return
    
    if used[cur]:
        dfs(cur+1, used, A, B)
    else:
        if A:
            if cur%W != W-1 and not used[cur+1]:
                used[cur] = True
                used[cur+1] = True
                dfs(cur+1, used, A-1, B)
                used[cur] = False
                used[cur+1] = False
            if cur + W < H*W and not used[cur+W]:
                used[cur] = True
                used[cur+W] = True
                dfs(cur+1, used, A-1, B)
                used[cur] = False
                used[cur+W] = False
        if B:
            used[cur] = True
            dfs(cur+1, used, A, B-1)
            used[cur] = False

H,W,A,B = map(int,input().split())

ans = 0
used = [False]*(H*W)
dfs(0,used,A,B)
print(ans)