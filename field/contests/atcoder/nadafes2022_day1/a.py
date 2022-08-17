N =int(input())

ans = 0
if N%2:
    ans = (N-1)*N//2 - 1
else:
    ans = (N-1)*N//2

print(ans)