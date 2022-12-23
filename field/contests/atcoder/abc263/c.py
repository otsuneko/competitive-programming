import itertools
N,M = map(int,input().split())

li = [i for i in range(1,M+1)]
ans = []
for ptr in itertools.permutations(li,N):
    pre = 0
    for p in ptr:
        if p < pre:
            break
        pre = p
    else:
        ans.append(tuple(ptr))
ans.sort()
for a in ans:
    print(*a)
