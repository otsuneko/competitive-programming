import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def max_score(H, W, K, S_i, S_j, A):
    import numpy as np

    # 0-based indexに変換
    S_i -= 1
    S_j -= 1

    # 初期位置
    current_dp = np.zeros((H, W), dtype=np.int64)
    current_dp[S_i][S_j] = A[S_i][S_j]

    def in_bounds(x, y):
        return 0 <= x < H and 0 <= y < W

    # 周期を見つけるための探索
    seen_states = {}
    state_list = []
    step = 0

    while step <= K:
        next_dp = np.zeros((H, W), dtype=np.int64)
        for i in range(H):
            for j in range(W):
                current_value = current_dp[i][j]
                if in_bounds(i-1, j):
                    next_dp[i-1][j] = max(next_dp[i-1][j], current_value + A[i-1][j])
                if in_bounds(i+1, j):
                    next_dp[i+1][j] = max(next_dp[i+1][j], current_value + A[i+1][j])
                if in_bounds(i, j-1):
                    next_dp[i][j-1] = max(next_dp[i][j-1], current_value + A[i][j-1])
                if in_bounds(i, j+1):
                    next_dp[i][j+1] = max(next_dp[i][j+1], current_value + A[i][j+1])
                next_dp[i][j] = max(next_dp[i][j], current_value + A[i][j])

        # 状態をタプルに変換して確認
        state_tuple = tuple(map(tuple, next_dp))

        if state_tuple in seen_states:
            cycle_start = seen_states[state_tuple]
            cycle_length = step - cycle_start
            break

        seen_states[state_tuple] = step
        state_list.append(next_dp)
        current_dp = next_dp
        step += 1
    else:
        # 周期を見つけられなかった場合はそのまま結果を返す
        return int(np.max(current_dp))

    # 周期を見つけた場合
    remaining_steps = (K - cycle_start) % cycle_length
    cycle_start_dp = state_list[cycle_start]
    for _ in range(remaining_steps):
        next_dp = np.zeros((H, W), dtype=np.int64)
        for i in range(H):
            for j in range(W):
                current_value = cycle_start_dp[i][j]
                if in_bounds(i-1, j):
                    next_dp[i-1][j] = max(next_dp[i-1][j], current_value + A[i-1][j])
                if in_bounds(i+1, j):
                    next_dp[i+1][j] = max(next_dp[i+1][j], current_value + A[i+1][j])
                if in_bounds(i, j-1):
                    next_dp[i][j-1] = max(next_dp[i][j-1], current_value + A[i][j-1])
                if in_bounds(i, j+1):
                    next_dp[i][j+1] = max(next_dp[i][j+1], current_value + A[i][j+1])
                next_dp[i][j] = max(next_dp[i][j], current_value + A[i][j])
        cycle_start_dp = next_dp

    return int(np.max(cycle_start_dp))

# 使用例
H,W,K = map(int,input().split())
S_i,S_j = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
print(max_score(H, W, K, S_i, S_j, A))
