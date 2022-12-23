import random
import time


pos = []
near_fromto = []
for i in range(1000):
    a,b,c,d = map(int,input().split())
    pos.append((a,b,c,d))

ans_R = []
ans_route = []
penalty = 10**18

start_t = time.time()

while 1:
    now_t = time.time()

    if now_t - start_t > 1.8:
        break

    shuffle_idx = random.sample([i for i in range(1000)],50)

    tmp_penalty = 0

    froms = []
    tos = []
    R = []
    for i in shuffle_idx:
        x1,y1,x2,y2 = pos[i]
        froms.append((x1,y1))
        tos.append((x2,y2))
        R.append(i+1)

    route = ["400 400"]
    start = [400,400]
    froms += [[-1,-1] for _ in range(50)]
    for i in range(100):

        min_dist = 10**18
        idx = -1

        for j in range(100):
            x,y = froms[j]
            if [x,y] == [-1,-1]:
                continue
            dist = abs(x-start[0]) + abs(y-start[1])

            if dist < min_dist:
                idx = j
                min_dist = dist

        if idx != -1:
            route.append(str(froms[idx][0]) + " " + str(froms[idx][1]))
            start = froms[idx][:]
            froms[idx] = [-1,-1]
            if idx < 50:
                # 次がfromのとき
                froms[idx+50] = tos[idx]
            tmp_penalty += min_dist

    if len(route) == 101 and tmp_penalty < penalty:
        penalty = tmp_penalty
        ans_R = R[:]
        ans_route = route[:]

ans_route.append("400 400")
print(50, *ans_R)
print(102, *ans_route)