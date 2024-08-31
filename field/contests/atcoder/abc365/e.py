import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def calculate_xor_sum(A):
    xor_sum = 0

    # 各ビット位置について0と1の数をカウント
    for bit in range(32):  # 32ビット整数と仮定
        count_ones = sum((a >> bit) & 1 for a in A)
        count_zeros = N - count_ones
        # 各ビット位置におけるペアの数を合計
        xor_sum += count_ones * (count_zeros << bit)

    return xor_sum

N = int(input())
A = list(map(int,input().split()))
print(calculate_xor_sum(A))
