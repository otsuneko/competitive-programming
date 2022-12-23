N = int(input())
prev = int(input())
for _ in range(N-1):
    today = int(input())

    if today == prev:
        print("stay")
    elif today > prev:
        print("up " + str(today-prev))
    else:
        print("down " + str(prev-today))
    prev = today