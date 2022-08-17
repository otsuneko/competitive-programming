import random
N = int(input())

masu = [0]*(N**2)
cnt = 1
for y in range(0,N,2):
    for x in range(N):
        idx = y*N+x
        masu[idx] = cnt
        cnt += 1
for y in range(1,N,2):
    for x in range(N):
        idx = y*N+x
        masu[idx] = cnt
        cnt += 1

# print(masu)
move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
def judge(masu,out):

    flg = True
    res = []
    if out:
        for idx in out:
            if (N<=idx<N**2-N) and idx%N != 0 and idx%N != N-1:
                y,x = idx//N,idx%N
                more,less = 0,0
                for dy,dx in move:
                    ny,nx = y+dy,x+dx
                    nidx = ny*N + nx
                    if masu[idx] > masu[nidx]:
                        more += 1
                    else:
                        less += 1
                if more == less:
                    res.append(idx)
                    flg = False
    else:
        for idx in range(N**2):
            if (N<=idx<N**2-N) and idx%N != 0 and idx%N != N-1:
                y,x = idx//N,idx%N
                more,less = 0,0
                for dy,dx in move:
                    ny,nx = y+dy,x+dx
                    nidx = ny*N + nx
                    if masu[idx] > masu[nidx]:
                        more += 1
                    else:
                        less += 1
                if more == less:
                    res.append(idx)
                    flg = False
    return flg,res

out = []
outs = 10**18
while 1:

    flg,out = judge(masu,out)
    if flg:
        break

    # 乱数でマスの値を変更
    idxs = out[:2]
    # print(idxs)

    change = []
    nidx = 0
    while 1:
        dy,dx = random.randint(-1,1),random.randint(-1,1)
        if len(idxs) == 1:
            y,x = idxs[0]//N,idxs[0]%N
            ny,nx = y+dy,x+dx
            nidx = ny*N+nx
            if len(change) == 1 and nidx not in change:
                change.append(nidx)
                break
            elif len(change) == 0:
                change.append(nidx)
        else:
            for idx in idxs:
                y,x = idx//N,idx%N
                ny,nx = y+dy,x+dx
                nidx = ny*N+nx
                change.append(nidx)
            if len(set(change)) != 1:
                break

    # print(change)
    masu[change[0]],masu[change[1]] = masu[change[1]],masu[change[0]]

    flg,out = judge(masu,out)
    if len(out) <= outs:
        outs = len(out)
    else:
        masu[change[0]],masu[change[1]] = masu[change[1]],masu[change[0]]
    # print(outs)

for i in range(N):
    print(*masu[i*N:i*N+N])