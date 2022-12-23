N = int(input())
A = list(map(int,input().split()))


# A1円払う場合
cost = [10**18]*N
cost[0],cost[1] = A[0],A[0]
feed = [False]*N
feed[0],feed[1] = True,True
for i in range(2,N):
    if feed[i] == False:
        if A[i-1] < A[i]:
            cost[i] = cost[i-1] + A[i]
            cost[i+1] = cost[i]
            feed[i] = True
            feed[i+1] = True
            cost[i] = cost[i-1] + A[i]
            cost[i+1] = cost[i]
            feed[i+1] = True
        else:
            cost[i+1] = cost[i-1] + A[i+1]
            feed[i+1] = True
            if i+2 < N:
                cost[i+2] = cost[i+1]
                feed[i+2] = True
# print(cost)
# print(feed)


# A1円払わない場合
# A1円払う場合
cost2 = [10**18]*N
cost2[0],cost2[-1] = A[-1],A[-1]
feed2 = [False]*N
feed2[0],feed2[-1] = True,True
for i in range(N-1):
    if feed[i+1] == False:
        cost2[i+1] = cost2[i] + A[i+1]
        feed2[i+1] = True
    else:
        if A[i] < A[i+1]:
            cost2[i] = cost2[i-1] + A[i]
            cost2[i+1] = cost2[i]
            feed2[i+1] = True
        else:
            cost2[i+1] = cost2[i-1] + A[i+1]
            feed2[i+1] = True
            if i+2 < N:
                cost2[i+2] = cost2[i+1]
                feed2[i+2] = True

print(cost2)
print(feed2)

print(min(cost[-1],cost2[-1]))