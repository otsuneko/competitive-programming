N = int(input())
A = list(map(int,input().split()))
mod = 10**9+7

ans = 1
cnt = [0,0,0]
for a in A:
    ans = ans*cnt.count(a)%mod
    for i in range(3):
        if cnt[i] == a:
            cnt[i] += 1
            break
print(ans)