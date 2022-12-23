A,B,K =map(int,input().split())

ans = 0
slime = A
while slime < B:
    ans += 1
    slime *= K

print(ans)