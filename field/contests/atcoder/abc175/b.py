N = int(input())
L = list(map(int,input().split()))

ans = 0
for i in range(N):
    for j in range(i+1,N):
        for k in range(j+1,N):
            L2 = [L[i],L[j],L[k]]
            if len(set(L2)) == 3:
                L2 = sorted(L2)
                if L2[0]+L2[1] > L2[2]:
                    ans += 1
print(ans)