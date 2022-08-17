A,B,C,X,Y =map(int,input().split())

# cost1 = A*X + B*Y
# cost2 = 2*C*max(X,Y)
# cost3 = 2*C*Y + A*(X-Y) if X > Y else 2*C*X + B*(Y-X)

# print(min(cost1,cost2,cost3))

ans = 10**18
for ab in range(0,max(X,Y)*2+1,2):
    cost = ab*C
    cost += A*(max(0,X-ab//2))
    cost += B*(max(0,Y-ab//2))

    ans = min(ans,cost)

print(ans)