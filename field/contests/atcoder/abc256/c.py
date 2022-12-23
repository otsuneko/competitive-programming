li = list(map(int,input().split()))
H = li[:3]
W = li[3:]

ans = 0
for i in range(1,H[0]-1):
    for j in range(1,H[0]-i):
        k = H[0]-i-j
        for l in range(1,H[1]-1):
            for m in range(1,H[1]-l):
                n = H[1]-l-m
                o,p,q = W[0]-i-l, W[1]-j-m,W[2]-k-n
                if o>0 and p>0 and q>0 and o+p+q == H[2]:
                    # print(i,j,k,l,m,n,o,p,q)
                    ans += 1
print(ans)