import sys
sys.setrecursionlimit(10**7)
import time
import random
from heapq import heappush, heappop
from collections import deque

import numpy as np
from scipy.ndimage import rotate

# 定数
TIME_LIMIT = 4.0
INF = 10**18


class Solver:

    def __init__(self, N: int, water_pos: List[Pos], house_pos: List[Pos], C: int):
        self.N = N
        self.water_pos = water_pos
        self.house_pos = house_pos
        self.C = C

    def is_block_contained(small_block, big_block):
        '''
        2つの3次元ブロックが包含関係にあるかどうかを判定する関数
        
        Parameters
        ----------
        small_block : list or numpy array
            小さいブロックの3次元配列
        big_block : list or numpy array
            大きいブロックの3次元配列
        '''
        # 大きいブロックの各座標について比較する
        for x in range(big_block.shape[0] - small_block.shape[0] + 1):
            for y in range(big_block.shape[1] - small_block.shape[1] + 1):
                for z in range(big_block.shape[2] - small_block.shape[2] + 1):
                    is_match = True
                    
                    # 小さいブロックの各座標について比較する
                    for i in range(small_block.shape[0]):
                        for j in range(small_block.shape[1]):
                            for k in range(small_block.shape[2]):
                                if small_block[i][j][k] != big_block[x+i][y+j][z+k]:
                                    is_match = False
                                    break
                            if not is_match:
                                break
                        if not is_match:
                            break
                    if is_match:
                        return True
                    
        # どの座標でも一致しなかった場合は包含されていないと判定する
        return False
    
    def rotate_x(block):
        return rotate(block, angle=90, axes=(0,1), reshape=True)

    def rotate_y(block):
        return rotate(block, angle=90, axes=(0,2), reshape=True)

    def rotate_z(block):
        return rotate(block, angle=90, axes=(1,2), reshape=True)

def main():
    N,W,K,C = map(int,input().split())
    water_pos = []
    house_pos = []
    for _ in range(W):
        y,x = map(int,input().split())
        water_pos.append(Pos(y,x))
    for _ in range(K):
        y,x = map(int,input().split())
        house_pos.append(Pos(y,x))

    solver = Solver(N, water_pos, house_pos, C)
    solver.solve()


if __name__ == "__main__":
    main()
