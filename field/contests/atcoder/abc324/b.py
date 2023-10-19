import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

for y in range(50):
    N2 = N
    if N2%(3**y) != 0:
        continue
    N2 //= (3**y)
    # print(N2)
    while N2 > 1:
        if N2%2 == 0:
            N2 //= 2
        else:
            break
    else:
        print("Yes")
        exit()
print("No")