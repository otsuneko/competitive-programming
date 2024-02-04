import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

v = "ABCDE"

S = list(input())
T = list(input())

S.sort()
T.sort()

S = "".join(S)
T = "".join(T)

one = {"AB","BC","CD","DE","AE"}
two = {"AC","AD","BD","BE","CE"}

if S in one and T in one:
    print("Yes")
elif S in two and T in two:
    print("Yes")
else:
    print("No")