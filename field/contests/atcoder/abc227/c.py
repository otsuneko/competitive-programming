import math
N = int(input())

ans = 0
L = math.ceil(pow(N,1/3))+1
ans = 0
for a in range(1,L+1):
    for b in range(a,N+1):
        c = N//(a*b)
        if c >= b and a*b*c <= N:
            ans += c-b+1
        else:
            break
print(ans)