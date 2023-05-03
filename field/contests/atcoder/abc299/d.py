N = int(input())
S = [-1]*(N+1)
S[1] = 0
S[N] = 1

ok = N
ng = 0
while (abs(ok - ng) > 1):
    ans = (ok + ng) // 2
    print("?",ans,flush=True)
    res = int(input())
    S[ans] = res
    if res == 1:
        ok = ans
    else:
        ng = ans

for i in range(1,N):
    if (S[i],S[i+1]) in [(0,1),(1,0)]:
        print("!",i)
        exit()