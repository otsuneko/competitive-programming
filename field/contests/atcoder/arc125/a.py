N,M = map(int,input().split())
S = list(map(int,input().split()))
T = list(map(int,input().split()))

if not set(T).issubset(set(S)):
    print(-1)
    exit()

if set(S) == set(T) and len(set(S)) == 1:
    print(N)
    exit()

min_move = min(S.index((S[0]+1)%2), S[::-1].index((S[0]+1)%2)+1)

ans = 0
cur = S[0]
first = True
for t in T:
    if t == cur:
        ans += 1
    elif first:
        ans += min_move + 1
        cur = (cur+1)%2
        first = False
    else:
        ans += 2
        cur = (cur+1)%2
print(ans)