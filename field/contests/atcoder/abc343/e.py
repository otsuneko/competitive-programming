import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def pair_overalapped_area(a1,b1,c1,a2,b2,c2):
    area = 1
    area *= max(0, min(a1,a2)+7 - max(a1,a2))
    area *= max(0, min(b1,b2)+7 - max(b1,b2))
    area *= max(0, min(c1,c2)+7 - max(c1,c2))
    return area

def trio_overlapped_area(a1,b1,c1,a2,b2,c2,a3,b3,c3):
    area = 1
    area *= max(0, min(a1,a2,a3)+7 - max(a1,a2,a3))
    area *= max(0, min(b1,b2,b3)+7 - max(b1,b2,b3))
    area *= max(0, min(c1,c2,c3)+7 - max(c1,c2,c3))
    return area

V1,V2,V3 =  map(int,input().split())

a1,b1,c1 = 0,0,0
for a2 in range(-1,8):
    for b2 in range(8):
        for c2 in range(8):
            for a3 in range(8):
                for b3 in range(8):
                    for c3 in range(8):
                        # ３つが重なる体積
                        v3 = trio_overlapped_area(a1,b1,c1,a2,b2,c2,a3,b3,c3)
                        if v3 != V3:
                            continue
                        # ２つが重なる体積
                        v2 = 0
                        # 1と2
                        v2 += pair_overalapped_area(a1,b1,c1,a2,b2,c2)
                        # 1と3
                        v2 += pair_overalapped_area(a1,b1,c1,a3,b3,c3)
                        # 2と3
                        v2 += pair_overalapped_area(a2,b2,c2,a3,b3,c3)
                        v2 -= v3*3
                        if v2 != V2:
                            continue
                        v1 = (7*7*7)*3 - (v2 * 2) - (v3 * 3)
                        if v1 == V1:
                            print("Yes")
                            print(a1,b1,c1,a2,b2,c2,a3,b3,c3)
                            exit()
print("No")
