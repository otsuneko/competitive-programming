import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T = map(str,input().split())
N = int(N)

S = [list(input()) for _ in range(N)]

former = [set() for _ in range(len(T))]
latter = [set() for _ in range(len(T))]

for i,s in enumerate(S):
    idx = 0
    for c in s:
        if idx == len(T):
            break
        if c == T[idx]:
            former[idx].add(i)
            idx += 1
    
    idx = 0
    s.reverse()
    for c in s:
        if idx == len(T):
            break
        if c == T[len(T)-1-idx]:
            latter[len(T)-1-idx].add(i)
            idx += 1
# print(former)
# print(latter)

ans = 0
for i in range(len(T)-1):
    f = former[i]
    l = latter[i+1]
    print(f,l)
    for c in f:
        ans += len(l-set([c]))
print(ans)