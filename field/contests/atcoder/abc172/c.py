from collections import deque
N,M,K = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

time = 0
cnt_A = 0
while cnt_A < N and time + A[cnt_A] <= K:
    time += A[cnt_A]
    cnt_A += 1

ans = cnt_A
cnt_B = 0
for i in range(cnt_A-1,-2,-1):

    while cnt_B < M and time + B[cnt_B] <= K:
        time += B[cnt_B]
        cnt_B += 1
    ans = max(ans,i+1+cnt_B)

    time -= A[i]

print(ans)