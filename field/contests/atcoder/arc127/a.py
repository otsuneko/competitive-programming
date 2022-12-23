N = int(input())

ans = 0
for i in range(len(str(N))):
    for j in range(10**i):
        if 10**i + j >= 2*10**i:
            break
        ans += str(10**i + j)