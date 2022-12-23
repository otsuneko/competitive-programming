from collections import defaultdict
dict = defaultdict(int)

N =int(input())
S = set([tuple(map(int,input().split())) for _ in range(N)])
T = set([tuple(map(int,input().split())) for _ in range(N)])

if S == T:
    print("Yes")
    exit()

cnt_Sx = defaultdict(int)
cnt_Sy = defaultdict(int)
cnt_Tx = defaultdict(int)
cnt_Ty = defaultdict(int)
for x,y in S:
    cnt_Sx[x] += 1
    cnt_Sy[y] += 1
for x,y in T:
    cnt_Tx[x] += 1
    cnt_Ty[y] += 1

if cnt_Sx != cnt_Tx and cnt_Sy != cnt_Ty:
    print("No")

elif cnt_Sx == cnt_Tx:
    sort_cnt_Sy = sorted(cnt_Sy.items(), key=lambda x:x[1])
    sort_cnt_Ty = sorted(cnt_Ty.items(), key=lambda x:x[1])
    cnt_Sy = defaultdict(int)
    cnt_Ty = defaultdict(int)
    for key,val in sort_cnt_Sy:
        cnt_Sy[key] = val
    for key,val in sort_cnt_Ty:
        cnt_Ty[key] = val

    lines = set()
    for key1 in cnt_Sy:
        for key2 in cnt_Ty:
            if cnt_Sy[key1] != cnt_Ty[key2]:
                break
            lines.add((key1 + key2)/2)
        if len(lines):
            break
    
    for line in lines:
        for key1 in cnt_Sy:
            key2 = 2*line-key1
            if cnt_Ty[key2] != cnt_Sy[key1]:
                break
        else:
            print("Yes")
            exit()
    print("No")

elif cnt_Sy == cnt_Ty:
    sort_cnt_Sx = sorted(cnt_Sx.items(), key=lambda x:x[1])
    sort_cnt_Tx = sorted(cnt_Tx.items(), key=lambda x:x[1])
    cnt_Sx = defaultdict(int)
    cnt_Tx = defaultdict(int)
    for key,val in sort_cnt_Sx:
        cnt_Sx[key] = val
    for key,val in sort_cnt_Tx:
        cnt_Tx[key] = val

    lines = set()
    for key1 in cnt_Sx:
        for key2 in cnt_Tx:
            if cnt_Sx[key1] != cnt_Tx[key2]:
                break
            lines.add((key1 + key2)/2)
        if len(lines):
            break
    
    for line in lines:
        for key1 in cnt_Sx:
            key2 = 2*line-key1
            if cnt_Tx[key2] != cnt_Sx[key1]:
                break
        else:
            print("Yes")
            exit()
    print("No")