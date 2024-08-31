from typing import List
import sys
import time
import random

# 定数
TIME_LIMIT = 4.0

N, M, T = map(int, input().split())
SEED_COUNT = 2 * N * (N - 1)
X = []

# 最初の種受取
for i in range(SEED_COUNT):
    X.append(list(map(int, input().split())))

# 種を強さ順にソート
def sort_seed(X):
    strength = [0] * SEED_COUNT

for t in range(T):
    # 種を植える場所
    A = [[0] * N for i in range(N)]

    # 種を植える
    for i in range(N):
        for j in range(N):
            A[i][j] = i * N + j

    for i in range(N):
        print(' '.join(map(str, A[i])), flush=True)

    # 配合後の種受取
    X = []
    for i in range(SEED_COUNT):
        X.append(list(map(int, input().split())))
