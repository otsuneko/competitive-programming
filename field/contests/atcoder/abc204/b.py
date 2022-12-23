N = int(input())
A = list(map(int,input().split()))

ans = 0
for a in A:
    add = a-10 if a-10>0 else 0
    ans += add
print(ans)