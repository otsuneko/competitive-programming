X = int(input())

for a in range(-1000,1000):
    for b in range(-1000,1000):
        if a**5 - b**5 == X:
            print(a,b)
            exit()