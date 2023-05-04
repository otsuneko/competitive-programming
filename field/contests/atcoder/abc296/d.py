N,M = map(int,input().split())

rt = int(M**0.5)+1

ans = 10**18
for a in range(1,rt+1):
    b = -(-(M)//a)
    if a <= N and b <= N and a*b >= M:
        ans = min(ans,a*b)

print(ans if ans != 10**18 else -1)