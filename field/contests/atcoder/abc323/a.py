import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

for i in range(1,16):
    if i%2 and S[i] != "0":
        print("No")
        exit()
print("Yes")