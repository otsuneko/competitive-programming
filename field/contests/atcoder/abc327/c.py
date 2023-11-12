import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A =  [list(map(int,input().split())) for _ in range(9)]

inv = list(zip(*A))

for y in range(9):
    if len(set(A[y])) != 9:
        print("No")
        exit()

for y in range(9):
    if len(set(inv[y])) != 9:
        print("No")
        exit()

s = [[set() for _ in range(3)] for _ in range(3)]
for y in range(9):
    for x in range(9):
        s[y//3][x//3].add(A[y][x])

for y in range(3):
    for x in range(3):
        if len(s[y][x]) != 9:
            print("No")
            exit()
print("Yes")