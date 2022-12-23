N = int(input())
A = list(map(int,input().split()))

B = [0]*N
total_A = sum(A)
total_B = 0
while 1:
    for i in range(1,N-1):
        if total_B < total_A:
            B[i] += 1
            total_B += 1
        else:
            break
    else:
        continue
    break

ans = 0
for i in range(N-1):
    ans += (1+(B[i+1]-B[i])**2)**0.5

print(ans)