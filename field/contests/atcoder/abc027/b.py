N =int(input())
A =list(map(int,input().split()))

if sum(A)%N:
    print(-1)
    exit()

avg = sum(A)//N

ans = 0
start = 0
total = 0
flg = False # 移動が必要な島か
for i in range(N):
    if flg == False:
        if A[i] == avg:
            continue
        else:
            flg = True
            start = i
            total += A[i]
    else:
        total += A[i]
        if total%(i-start+1) == 0 and total//(i-start+1) == avg:
            ans += i-start
            flg = False
            total = 0

print(ans)