import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

if S in ["ACE","BDF","CEG","DFA","EGB","FAC","GBD"]:
    print("Yes")
else:
    print("No")