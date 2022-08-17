import itertools
N = int(input())
happiness = [[0]*N for _ in range(N)]

ans = 0
for i in range(N-1):
    tmp = list(map(int,input().split()))
    for j in range(len(tmp)):
        happiness[i][i+j+1] = tmp[j]
        happiness[i+j+1][i] = tmp[j]
    # 1グループの場合
    ans += sum(tmp)

# print(*happiness, sep="\n")

# 2グループの場合
seq = (0,1)
all = itertools.product(seq, repeat=N)
for ptr in all:
    group = [[] for _ in range(2)]
    for i in range(N):
        if ptr[i] == 0:
            group[0].append(i)
        elif ptr[i] == 1:
            group[1].append(i)

    tmp_ans = 0
    for g in group:
        if len(g) <= 1:
            continue
        for i in range(len(g)):
            for j in range(i+1,len(g)):
              tmp_ans += happiness[g[i]][g[j]]
    
    ans = max(ans,tmp_ans)

# 3グループの場合
seq = (0,1,2)
all = itertools.product(seq, repeat=N)
for ptr in all:
    group = [[] for _ in range(3)]

    for i in range(N):
        if ptr[i] == 0:
            group[0].append(i)
        elif ptr[i] == 1:
            group[1].append(i)
        elif ptr[i] == 2:
            group[2].append(i)
    tmp_ans = 0
    for g in group:
        if len(g) <= 1:
            continue
        for i in range(len(g)):
            for j in range(i+1,len(g)):
              tmp_ans += happiness[g[i]][g[j]]

    ans = max(ans,tmp_ans)

print(ans)