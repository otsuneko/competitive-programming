N = int(input()) + 1
A = [0] + list(map(int,input().split()))

ball = [0]*N

for i in range(N-1,(N-1)//2,-1):
    ball[i] = A[i]

for i in range((N-1)//2,0,-1):
    j = i
    cnt = 0
    mul = 1
    while j*mul < N:
        cnt += ball[j*mul]
        mul += 1
    if cnt%2 != A[i]:
        ball[i] = 1

ans = sum(ball[1:])
li = []
for i,b in enumerate(ball):
    if b == 1:
        li.append(i)

print(ans)
if ans > 0:
    print(*li)