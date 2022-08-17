A,B,C,X =map(int,input().split())

ans = 1.0
if X <= A:
    pass
elif A < X < B+1:
    ans = C/(B-A)
else:
    ans = 0.0
print(ans)