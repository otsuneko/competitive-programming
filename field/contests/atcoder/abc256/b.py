N = int(input())
A = list(map(int,input().split()))
koma = [False]*4

P = 0
for a in A:
    koma[0] = True
    for i in range(3,-1,-1):
        if koma[i]:
            if i+a >= 4:                
                P += 1
            else:
                koma[i+a] = True
            koma[i] = False
print(P)