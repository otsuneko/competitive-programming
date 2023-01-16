N = int(input())
S = input()

ans = [0]*(N-1)
for i in range(N-1):
    cnt = 0
    for j in range(N-1-i):
        if S[j] == S[j+i+1]:
            break
        else:
            cnt += 1
    ans[i] = cnt

for a in ans:
    print(a)