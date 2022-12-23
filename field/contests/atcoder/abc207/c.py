N = int(input())
# ans_list = [True]*N

range_ = []
for i in range(N):
    t,l,r = map(int,input().split())
    if t == 1:
        range_.append([l,r])
    elif t == 2:
        range_.append([l,r-0.5])
    elif t == 3:
        range_.append([l+0.5,r])
    elif t == 4:
        range_.append([l+0.5,r-0.5])

# print(range_)
ans = 0
for i in range(N):
    for j in range(i+1,N):
        if range_[i][1] > range_[j][1]:
            if range_[i][0] <= range_[j][1]:
                ans += 1
        else:
            if range_[i][1] >= range_[j][0]:
                ans += 1

print(ans)