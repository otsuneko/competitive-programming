from heapq import heappush, heappop
import List
inf=10**18
DIR = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
INV_DIR = {(-1,0):"U", (0,1):"R", (1,0):"D", (0,-1):"L"}

H = W = 20
NUM = 100
TURN_LIMIT = 4000
graph = [[-1]*W for _ in range(H)]

class State:
    def __init__(self, NUM: int, H: int, W: int, Cards: List[List[int]]):
        self.NUM = NUM
        self.H = H
        self.W = W
        self.turn = 0
        self.Cards = Cards
        self.ans = []

        # 現在地
        self.cur_y, self.cur_x = 0,0
        # 山札
        self.deck = []
        # グリッドの状態(-1が何も置いてない)
        self.grid = [[[-1] for _ in range(W)] for _ in range(H)]
        for i,y,x in enumerate(Cards):
            self.grid[y][x] = i

    # 移動に伴う更新
    def move(self,y,x,ny,nx):
        assert 0<=y<H and 0<=x<W and 0<=ny<H and 0<=nx<W
        dy,dx = ny-y,nx-x
        if dy==0:
            dx 


    # カードの取得
    def input_card(self,y,x):
        assert self.grid[y][x] >= 0
        self.ans.append("I")
        self.deck.append(self.grid[y][x])
        self.grid[y][x] = -1
    
    # カードの設置
    def output_card(self,y,x):
        assert self.grid[y][x] == -1
        self.ans.append("O")
        self.grid[y][x] = self.deck.pop()

class Solver:

    def __init__(self, NUM: int, H: int, W: int, Cards: List[List[int]]):
        self.NUM = NUM
        self.H = H
        self.W = W
        self.cards = Cards
        self.state = State(NUM,H,W,Cards)


    def solve(self) -> None:
        # カードまでの移動経路を求める
        self.

        # 解の出力
        print("".join("".join(self.state.ans)))

def main():
    Cards = [[-1,-1] for _ in range(NUM)]
    for i in range(100):
        x,y = map(int,input().split())
        Cards[i] = [x,y]
    solver = Solver(NUM,H,W,Cards)
    solver.solve()

if __name__ == "__main__":
    main()