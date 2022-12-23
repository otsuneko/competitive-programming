from operator import itemgetter
import math
from decimal import Decimal

def calc_angle(vector1, vector2):

    length1 = math.sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
    length2 = math.sqrt(vector2[0] * vector2[0] + vector2[1] * vector2[1])

    inner = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (length1 * length2)

    if 1 < inner or inner < -1:
        return 0

    return math.acos((vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (length1 * length2))

N = int(input())
S = []
for _ in range(N):
    S.append(list(map(int,input().split())))

T = []
for _ in range(N):
    T.append(list(map(int,input().split())))

origin = S[0]

vec = [[0,0]]*(N-1)
for i in range(1,N):
    vec[i-1] = [S[i][0]-origin[0], S[i][1]-origin[1]]

vec_t = [[0,0]]*(N-1)
for i in range(N):
    origin_t = T[i]
    idx = 0
    for j in range(N):
        if i == j:
            continue
        vec_t[idx] = [T[j][0]-origin_t[0],T[j][1]-origin_t[1]]
        idx += 1

    for j in range(N-1):
        #回転角度(radian)
        angle = calc_angle(vec[0],vec_t[j])
        check = set([])
        for k in range(N-1):
            #回転前の座標
            x = vec[k][0]
            y = vec[k][1]
            #回転中心の座標(原点の場合は0)
            center_x = origin[0]
            center_y = origin[1]
            #回転後の座標 
            X = math.cos(angle) * (x - center_x) - math.sin(angle) * (y - center_y) + center_x
            Y = math.sin(angle) * (x - center_x) + math.cos(angle) * (y - center_y) + center_y

            if [int(X),int(Y)] not in vec_t:
                break
        else:
            print("Yes")
            exit()

print("No")