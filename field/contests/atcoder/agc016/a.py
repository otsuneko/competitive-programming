import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

ans = INF
alphabet = "abcdefghijklmnopqrstuvwxyz"

for i in range(26):
    c = alphabet[i]
    if c not in S:
        continue
    T = S[:]
    cnt = 0
    while 1:
        if T.count(c) == len(T):
            break
        T2 = []
        for i in range(len(T)-1):
            if T[i] == c or T[i+1] == c:
                T2.append(c)
            else:
                T2.append(T[i])
        T = T2[:]
        cnt += 1
    
    ans = min(ans,cnt)

print(ans)