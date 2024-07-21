A,B = map(int,input().split())

for i in range(B,0,-1):
    ini = -(-(A)//i) * i

    cnt = 0
    while ini <= B and cnt < 2:
        ini += i
        cnt += 1
    if cnt == 2:
        print(i)
        exit()
