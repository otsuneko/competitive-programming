import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
H = list(map(int,input().split()))

T = 0
for h in H:
    while T%3 != 0 and h > 0:
        T += 1
        if T%3 == 0:
            h -= 3
        else:
            h -= 1

    add = h//5
    T += 3 * add
    h -= 5 * add

    while h > 0:
        T += 1
        if T%3 == 0:
            h -= 3
        else:
            h -= 1

print(T)
