N =int(input())
P =list(map(int,input().split()))
Q =list(map(int,input().split()))

i = j = 0

ans = 0
idx = 0
while j < N:
    while i < N:
        if Q[i]%P[i] == 0:
            i += 1
            j += 1
            ans += 1
            idx = i
        else:
            i += 1
    i = idx
    j += 1

print(ans)