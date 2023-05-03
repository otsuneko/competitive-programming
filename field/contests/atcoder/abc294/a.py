N = int(input())
A = list(map(int,input().split()))

ans = []
for n in A:
    if n%2==0:
        ans.append(n)
print(*ans)