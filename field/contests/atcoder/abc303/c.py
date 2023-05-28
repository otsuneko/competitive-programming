N,M,H,K = map(int,input().split())
S = input()
items = set()
for i in range(M):
    tmp = tuple(map(int,input().split()))
    items.add(tmp)

DIR = {"R":(1,0), "U":(0,1), "L":(-1,0), "D":(0,-1)}
cur = [0,0]
for i in range(N):
    nx,ny = cur[0]+DIR[S[i]][0], cur[1]+DIR[S[i]][1]
    H -= 1

    if H >= 0:
        if (nx,ny) in items and H < K:
            H = K
            items.remove((nx,ny))
    else:
        print("No")
        exit()
    cur = [nx,ny]
    # print(cur,H)

if H < 0:
    print("No")
else:
    print("Yes")