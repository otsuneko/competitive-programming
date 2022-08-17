N = int(input())

for money in range(1,50000):
    if int(money * 1.08) == N:
        print(money)
        break
else:
    print(":(")