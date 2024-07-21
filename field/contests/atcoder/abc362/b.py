import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import math

def is_right_triangle(p1, p2, p3):
    def distance_sq(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    # 各点間の距離の2乗を計算する
    d1 = distance_sq(p1, p2)
    d2 = distance_sq(p2, p3)
    d3 = distance_sq(p3, p1)

    # 三つの距離のリストを作成し、ソートする
    distances = sorted([d1, d2, d3])

    # ピタゴラスの定理をチェックする
    return math.isclose(distances[0] + distances[1], distances[2])

# 三つの点の座標を入力
p1 = list(map(int,input().split()))
p2 = list(map(int,input().split()))
p3 = list(map(int,input().split()))

# 直角三角形かどうかを判定
if is_right_triangle(p1, p2, p3):
    print("Yes")
else:
    print("No")
