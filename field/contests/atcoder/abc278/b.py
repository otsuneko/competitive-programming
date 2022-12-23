H,M = map(int,input().split())

h1 = H//10
h2 = H%10
m1 = M//10
m2 = M%10

while 1:

    # 条件満たすか判定
    if 0 <= h1*10 + m1 < 24 and 0 <= h2*10 + m2 < 60:
        print(h1*10 + h2, m1*10 + m2)
        break

    m2 += 1
    if m2 >= 10:
        m1 += 1
        m2 = 0
        if m1 >= 6:
            h2 += 1
            m1 = 0
            if h2 >= 4 and h1 == 2:
                h1 = 0
                h2 = 0
            elif h2 >= 10:
                h1 += 1
                h2 = 0