import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

ans = S.replace("a","").replace("e","").replace("i","").replace("o","").replace("u","")
print(ans)