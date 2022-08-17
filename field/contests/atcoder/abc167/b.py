A,B,C,K = map(int,input().split())

ans = 0
card = 0
if A >= K:
    ans = K
    card = K
else:
    ans = A
    card = A

if card + B < K:
    ans -= K-(card+B)

print(ans)