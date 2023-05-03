H,W = map(int,input().split())
C = []
C.append(["."]*(W+2))
for h in range(H):
    tmp = ["."] + list(input()) + ["."]
    C.append(tmp)
C.append(["."]*(W+2))

N = min(H,W)
S = [0]*N
for n in range(1,N+1):
    for y in range(H+2):
        for x in range(W+2):
            for d in range(n+1):
                if not (1 <= y+d <= H and 1 <= y-d <= H and 1 <= x+d <= W and 1 <= x-d <= W and C[y+d][x+d] == C[y+d][x-d] == C[y-d][x+d] == C[y-d][x-d] == "#"):
                    break
            else:
                if (0<=y+n+1<=H and 0<=x+n+1<=W and C[y+n+1][x+n+1] == ".") or (0<=y+n+1<=H and 0<=x-n-1<=W and C[y+n+1][x-n-1] == ".") or (0<=y-n-1<=H and 0<=x+n+1<=W and C[y-n-1][x+n+1] == ".") or (0<=y-n-1<=H and 0<=x-n-1<=W and C[y-n-1][x-n-1] == "."):
                    # print(n,y,x)
                    S[n-1] += 1
print(*S)