N,Q,X = map(int,input().split())
W = list(map(int,input().split()))*(10**7//N)

box = []
tmp = []
su = 0
loop_start = 0
dic = dict()
for w in W:
    su += w
    tmp.append(w)
    if su >= X:
        ttmp = tuple(tmp)
        if ttmp in dic:
            loop_start = dic[ttmp]
            break
        box.append((len(ttmp),ttmp))
        dic[ttmp] = len(box)-1
        tmp = []
        su = 0

# print(box,loop_start)

for _ in range(Q):
    K = int(input())
    K -= 1
    if K <= loop_start:
        print(box[K][0])
    else:
        idx = loop_start + (K-loop_start)%(len(box)-loop_start)
        print(box[idx][0])