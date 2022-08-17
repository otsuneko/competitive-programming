H,W,K = map(int,input().split())
masu = [list(input()) for _ in range(H)]

import itertools
num = H+W #生成するビット数
bit_list = list(itertools.product([0, 1], repeat=num))

ans = 0
for bit in bit_list:
    bit_H = bit[:H]
    bit_W = bit[H:]

    cnt = 0
    for y in range(H):
        for x in range(W):
            if bit_H[y] != 1 and bit_W[x] != 1 and masu[y][x] == "#":
                cnt += 1
    
    if cnt == K:
        ans += 1

print(ans)