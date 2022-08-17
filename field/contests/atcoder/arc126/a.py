T = int(input())
for _ in range(T):
    N2,N3,N4 = map(int,input().split())

    ans = 0
    if N4 >= 1 and N3 >= 2:
        # print(1,N2,N3,N4)
        add = min(N4*2,N3)//2
        N4 -= add
        N3 -= add*2
        ans += add
    if N4 >= 2 and N2 >= 1:
        # print(3,N2,N3,N4)
        add = min(N4,N2*2)//2
        N4 -= add*2
        N2 -= add
        ans += add
    if N2 >= 2 and N3 >= 2:
        # print(5,N2,N3,N4)
        add = min(N2,N3)//2
        N2 -= add*2
        N3 -= add*2
        ans += add
    if N4 >= 1 and N2 >= 3:
        # print(4,N2,N3,N4)
        add = min(N4*3,N2)//3
        N4 -= add
        N2 -= add*3
        ans += add
    if N2 >= 5:
        # print(6,N2,N3,N4)
        add = N2//5
        N2 -= add*5
        ans += add
    print(ans)