import numpy as np

pos = [list(map(int,input().split())) for _ in range(4)]
pattern = ([0,1,2,],[1,2,3],[2,3,0],[3,0,1])

sum_deg = 0
for ptr in pattern:
    # 点A,B,Cの座標（3次元座標上の場合）
    a = np.array(pos[ptr[0]])
    b = np.array(pos[ptr[1]])
    c = np.array(pos[ptr[2]])

    # ベクトルを定義
    vec_a = a - b
    vec_c = c - b

    # コサインの計算
    length_vec_a = np.linalg.norm(vec_a)
    length_vec_c = np.linalg.norm(vec_c)
    inner_product = np.inner(vec_a, vec_c)
    cos = inner_product / (length_vec_a * length_vec_c)

    # 角度（ラジアン）の計算
    rad = np.arccos(cos)

    # 弧度法から度数法（rad ➔ 度）への変換
    degree = np.rad2deg(rad)
    # print(degree)
    if 0 < degree < 180:
        sum_deg += degree
        continue
    else:
        print("No")
        exit()

if abs(sum_deg-360) < 0.0001:
    print("Yes")
else:
    print("No")