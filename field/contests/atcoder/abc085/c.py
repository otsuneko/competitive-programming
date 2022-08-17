N,Y = map(int,input().split())

man = Y//10000

for i in range(man,-1,-1):
    gosen = (Y-i*10000)//5000
    for j in range(gosen,-1,-1):
        sen = (Y-i*10000-j*5000)//1000
        if i+j+sen == N:
            print(i,j,sen)
            exit()
print(-1,-1,-1)
