N = int(input())
A = list(map(int,input().split()))

color = set()
cnt = 0
for a in A:
    if a <= 399:
        color.add("gray")
    elif a <= 799:
        color.add("brown")
    elif a <= 1199:
        color.add("green")
    elif a <= 1599:
        color.add("cyan")
    elif a <= 1999:
        color.add("blue")
    elif a <= 2399:
        color.add("yellow")
    elif a <= 2799:
        color.add("orange")
    elif a <= 3199:
        color.add("red")
    else:
        cnt += 1

print(max(len(color),1),len(color)+cnt)
