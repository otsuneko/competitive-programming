a,b = map(int,input().split())

if a <= 0 and b >= 0:
    print("Zero")
elif b < 0:
    if (b-a)%2 == 0:
        print("Negative")
    else:
        print("Positive")
else:
    if a%2 == 0:
        print("Negative")
    else:
        print("Positive")