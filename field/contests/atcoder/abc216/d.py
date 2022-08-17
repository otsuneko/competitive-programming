import sys
sys.setrecursionlimit(10**7)
from collections import defaultdict

def delete_pair(key,k1,k2):
    global cnt
    
    top_list[key] = []
    idx[k1] += 1
    idx[k2] += 1

    if idx[k1] < k_list[k1]:
        top_list[balls[k1][idx[k1]]].append(k1) 
    if idx[k2] < k_list[k2]:
        top_list[balls[k2][idx[k2]]].append(k2)
    cnt += 2

    if idx[k1] < k_list[k1] and len(top_list[balls[k1][idx[k1]]]) == 2:
        nxt_k1,nxt_k2 = top_list[balls[k1][idx[k1]]][0], top_list[balls[k1][idx[k1]]][1]
        delete_pair(balls[k1][idx[k1]], nxt_k1, nxt_k2)

    if idx[k2] < k_list[k2] and len(top_list[balls[k2][idx[k2]]]) == 2:
        nxt_k1,nxt_k2 = top_list[balls[k2][idx[k2]]][0], top_list[balls[k2][idx[k2]]][1]
        delete_pair(balls[k2][idx[k2]], nxt_k1, nxt_k2)

N,M = map(int,input().split())

balls = []
top_list = defaultdict(list)
k_list = []
for i in range(M):
    k = int(input())
    k_list.append(k)
    balls.append(list(map(int,input().split())))
    top_list[balls[-1][0]].append(i)

idx = [0]*M
cnt = 0
while 1:
    cnt_pair = 0
    for key in list(top_list):
        if len(top_list[key]) == 2:
            k1,k2 = top_list[key]
            delete_pair(key,k1,k2)
            cnt_pair += 1
            
    if cnt == 2*N:
        print("Yes")
        exit()
    if cnt_pair == 0:
        print("No")
        exit()
