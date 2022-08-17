X,Y = map(int,input().split())

for shika in range(101):
    for tsuru in range(101):
        if shika+tsuru == X and shika*4+tsuru*2 == Y:
            print("Yes")
            exit()
print("No")