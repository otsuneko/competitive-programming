import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S,T = map(str,input().split())

for w in range(1,len(S)-1):
    li = []
    for c in range(0,len(S),w):
        li.append(S[c:min(len(S),c+w)])
    for c in range(len(li[0])):
        s = []
        for l in li:
            if c >= len(l):
                break
            s.append(l[c])
        if "".join(s) == T:
            print("Yes")
            exit()
print("No")
