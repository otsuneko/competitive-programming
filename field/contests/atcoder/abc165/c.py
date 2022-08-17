import itertools
N,M,Q = map(int,input().split())
cond = [list(map(int,input().split())) for _ in range(Q)]

seq = [i for i in range(1,M+1)]
cmb = itertools.combinations_with_replacement(seq, N)

ans = 0
for A in cmb:
    score = 0
    for c in cond:
        if A[c[1]-1] - A[c[0]-1] == c[2]:
            score += c[3]
    ans = max(ans, score)
print(ans)
