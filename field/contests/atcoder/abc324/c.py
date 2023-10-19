import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T = map(str,input().split())
N = int(N)

ans = []
for i in range(N):
    S = input()
    if len(S) == len(T):
        if S == T:
            ans.append(i+1)
        else:
            cnt = 0
            for j in range(len(S)):
                if S[j] != T[j]:
                    cnt += 1
            if cnt == 1:
                ans.append(i+1)
    elif len(S) == len(T)+1:
        flg = False
        for j in range(len(T)):
            if flg == False and S[j] != T[j]:
                if S[j+1] != T[j]:
                    break
                flg = True
            elif flg == True and S[j+1] != T[j]:
                break
        else:
            ans.append(i+1)
    elif len(S)+1 == len(T):
        flg = False
        for j in range(len(S)):
            if flg == False and S[j] != T[j]:
                if S[j] != T[j+1]:
                    break
                flg = True
            elif flg == True and T[j+1] != S[j]:
                break
        else:
            ans.append(i+1)

print(len(ans))
print(*ans)