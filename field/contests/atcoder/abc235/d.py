def rolling(s, n):
    l = len(s)
    #右にシフトの場合
    return s[-n%l:] + s[:-n%l] #左にシフトの場合はnの正負を逆に

# Pythonで提出！！
# from collections import defaultdict
# dict = defaultdict(int)
# import sys
# sys.setrecursionlimit(10**7)
# def dfs(a,x,N,cnt):
#     global ans

#     if len(str(x)) > len(str(N)):
#         return 10**18

#     if x == N:
#         ans = min(ans, cnt)
        
#     if dict[x*a] == 0 or cnt < dict[x*a]:
#         dict[x*a] = cnt
#         dfs(a,x*a,N,cnt+1)

#     if x >= 10 and x%10 != 0:
#         nxt = int(rolling(str(x),1))
#         if dict[nxt] == 0 or cnt < dict[nxt]:
#             dict[nxt] = cnt
#             dfs(a,nxt,N,cnt+1)

from collections import deque
from collections import defaultdict
cnt = defaultdict(int)
cnt2 = defaultdict(int)

def bfs(a,N):
    queue = deque()
    queue.append([1,0])
    pre = 0
    while queue:
        s = queue.popleft()

        if len(str(s[0])) > len(str(N)):
            cnt[s[1]] += 1
        cnt2[s[1]] += 1

        if s[1] != pre:
            if cnt[pre] == cnt2[pre]:
                return -1

        if s[0] == N:
            return s[1]
        if s[0] >= 10 and s[0]%10 != 0:
            nxt = int(rolling(str(s[0]),1))
            if nxt not in seen:
                seen.add(nxt)
                queue.append([nxt,s[1]+1])
        if s[0]*a not in seen:
            seen.add(s[0]*a)
            queue.append([s[0]*a,s[1]+1])
        
        pre = s[1]

a,N =map(int,input().split())
seen = set()
print(bfs(a,N))

# ans = 10**18
# dfs(a,1,N,0)
# if ans != 10**18:
#     print(ans)
# else:
#     print(-1)