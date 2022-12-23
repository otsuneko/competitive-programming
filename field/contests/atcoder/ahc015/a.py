candies = list(map(int,input().split()))

for t,candy in enumerate(candies):
    place = int(input())

    if candy == 1:
        print("L",flush=True)
    elif candy == 2:
        print("R",flush=True)
    elif candy == 3:
        print("B",flush=True)