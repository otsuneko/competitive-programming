N =int(input())
#C,S,F
time =[list(map(int,input().split())) for _ in range(N-1)]

ans = [0]*(N-1)
for i in range(N-1):
    for j in range(i,N-1):
        C,S,F = time[j]
        if ans[i] > S:
            ans[i] += -(-(ans[i]-S)//F)*F-(ans[i]-S)
        else:
            ans[i] += (S-ans[i])
        ans[i] += C

for a in ans:
    print(a)
print(0)