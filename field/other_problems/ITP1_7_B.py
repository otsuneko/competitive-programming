while 1:
    n,x = map(int,input().split())

    if [n,x] == [0,0]:
        break

    ans = 0
    for i in range(1,n):
        for j in range(i+1,n):
            k = x-i-j
            if j < k <= n:
                ans += 1
    print(ans)