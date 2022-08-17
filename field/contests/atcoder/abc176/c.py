N = int(input())
A = list(map(int,input().split()))

ans = 0
cur_height = 0
for a in A:
    if cur_height > a:
        ans += cur_height-a
    else:
        cur_height = a

print(ans)