security = [1,2,5,4,1,0,2,4,5,3,1,2,4,3,2,4,8]
time = 2

ans = []
if len(security) < 2*time+1:
    print(ans)

idx = set()
cnt = 0
for i in range(len(security)-1):
    if security[i+1] - security[i] <= 0:
        cnt += 1
    else:
        cnt = 0
    if cnt >= time:
        idx.add(i+1)

idx2 = set()
cnt = 0
security = security[::-1]
for i in range(len(security)-1):
    if security[i+1] - security[i] >= 0:
        cnt += 1
    else:
        cnt = 0
    if cnt >= time:
        idx.add(i+1)
print(idx2)
print(idx & idx2)