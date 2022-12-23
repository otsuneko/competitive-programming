N = int(input())
A = list(map(int,input().split()))
lim = max(A)+1

cnt = [0]*lim
ok = [True]*lim

for i in range(N):
    cnt[A[i]] += 1

for i in range(1,lim):
    if cnt[i]:
        if cnt[i] > 1:
            ok[i] = False
        for j in range(i*2, lim, i):
            ok[j] = False

ans = 0
for i in range(N):
    if ok[A[i]]:
        ans += 1
print(ans)