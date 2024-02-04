import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

for i in range(len(S)):
    if i == 0 and S[i].isupper() == False:
        print("No")
        exit()
    if i != 0 and S[i].islower() == False:
        print("No")
        exit()
print("Yes")