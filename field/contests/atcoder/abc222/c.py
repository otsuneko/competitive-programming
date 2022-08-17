N,M = map(int,input().split())
A = [list(input()) for _ in range(N*2)]

te = ["G","C","P"]
win = []
for i in range(2*N):
    win.append([0,i])

for i in range(M):
    for j in range(0,2*N,2):

        p1 = A[win[j][1]][i]
        p2 = A[win[j+1][1]][i]

        idx = 0
        for k in range(3):
            if p1 == te[k]:
                idx = k
                break
        
        if p2 == te[(idx+1)%3]:
            win[j][0] += 1
        elif p2 == te[idx]:
            pass
        else:
            win[j+1][0] += 1

    win.sort(key=lambda x:(-x[0],x[1]))

for p in win:
    print(p[1]+1)