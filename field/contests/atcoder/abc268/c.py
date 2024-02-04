N = int(input())
P = list(map(int,input().split()))
invP = dict()
roll_cnt = [0]*N

for i,p in enumerate(P):
    invP[p] = i

for i,p in enumerate(P):
    cur_idx = invP[i]
    roll = (i-1-cur_idx)%N
    for j in range(3):
        roll_cnt[(roll+j)%N] += 1
print(max(roll_cnt))
