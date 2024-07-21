MOD = 998244353

def popcount_sum(N, M):
    total_sum = 0
    bit_position = 0

    while M > 0:
        if M & 1:
            # For the current bit position, calculate the contribution
            full_groups = (N + 1) >> (bit_position + 1)
            remainder = (N + 1) & ((1 << (bit_position + 1)) - 1)
            count_of_ones = full_groups * (1 << bit_position) + max(0, remainder - (1 << bit_position))

            total_sum = (total_sum + count_of_ones) % MOD

        M >>= 1
        bit_position += 1

    return total_sum

# 標準入力からNとMを読み取る
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
M = int(data[1])

# 答えを計算して出力する
result = popcount_sum(N, M)
print(result)
