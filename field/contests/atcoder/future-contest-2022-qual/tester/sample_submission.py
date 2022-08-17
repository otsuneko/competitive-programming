from collections import namedtuple

DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]

Vegetable = namedtuple('Vegetable', ['r', 'c', 's', 'e', 'v'])


class Action:
    def __init__(self, vs):
        self.vs = vs

    @classmethod
    def create_pass(cls):
        return cls([-1])

    @classmethod
    def create_purchase(cls, r, c):
        return cls([r, c])

    @classmethod
    def create_move(cls, r1, c1, r2, c2):
        return cls([r1, c1, r2, c2])

    def __str__(self):
        return " ".join(str(v) for v in self.vs)


class Game:
    def __init__(self, n, t, veges):
        self.n = n
        self.has_machine = [[False] * n for _ in range(n)]
        self.vege_values = [[0] * n for _ in range(n)]
        self.next_price = 1
        self.num_machine = 0
        self.money = 1
        self.veges_start = [[] for _ in range(t)]  # veges_start[i] : vegetables appear on day i
        self.veges_end = [[] for _ in range(t)]    # veges_end[i] : vegetables disappear on day i
        for vege in veges:
            self.veges_start[vege.s].append(vege)
            self.veges_end[vege.e].append(vege)

    def purchase(self, r, c):
        assert not self.has_machine[r][c]
        assert self.next_price <= self.money
        self.has_machine[r][c] = True
        self.num_machine += 1
        self.money -= self.next_price
        self.next_price = (self.num_machine + 1) ** 3

    def move(self, r1, c1, r2, c2):
        assert self.has_machine[r1][c1]
        self.has_machine[r1][c1] = False
        assert not self.has_machine[r2][c2]
        self.has_machine[r2][c2] = True

    def simulate(self, day, action):
        # apply
        if len(action.vs) == 2:
            self.purchase(*action.vs)
        elif len(action.vs) == 4:
            self.move(*action.vs)
        # appear
        for vege in self.veges_start[day]:
            self.vege_values[vege.r][vege.c] = vege.v
        # harvest
        for r in range(self.n):
            for c in range(self.n):
                if self.has_machine[r][c] and self.vege_values[r][c] > 0:
                    self.money += self.vege_values[r][c] * self.count_connected_machines(r, c)
                    self.vege_values[r][c] = 0
        # disappear
        for vege in self.veges_end[day]:
            self.vege_values[vege.r][vege.c] = 0

    def count_connected_machines(self, r, c):
        queue = [(r, c)]
        visited = [[False] * self.n for _ in range(self.n)]
        visited[r][c] = True
        i = 0
        while i < len(queue):
            cr, cc = queue[i]
            for dir in range(4):
                nr = cr + DR[dir]
                nc = cc + DC[dir]
                if 0 <= nr < self.n and 0 <= nc < self.n and self.has_machine[nr][nc] and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
            i += 1
        return i

    def select_next_action(self, day):
        # implement your strategy here

        if self.money < self.next_price:
            return Action.create_pass()
        else:
            # search best place for a new machine
            sum_future_veges = [[0] * self.n for _ in range(self.n)]
            for i in range(day, len(self.veges_start)):
                for vege in self.veges_start[i]:
                    sum_future_veges[vege.r][vege.c] += vege.v
            max_sum = 0
            max_r = -1
            max_c = -1
            for r in range(self.n):
                for c in range(self.n):
                    if self.has_machine[r][c]:
                        continue
                    if max_sum < sum_future_veges[r][c]:
                        max_sum = sum_future_veges[r][c]
                        max_r = r
                        max_c = c
            if max_sum > 0:
                return Action.create_purchase(max_r, max_c)
            else:
                return Action.create_pass()


def main():
    N, M, T = list(map(int, input().split()))
    veges = []
    for _ in range(M):
        r, c, s, e, v = list(map(int, input().split()))
        veges.append(Vegetable(r, c, s, e, v))
    game = Game(N, T, veges)
    actions = []
    for day in range(T):
        action = game.select_next_action(day)
        actions.append(action)
        game.simulate(day, action)

    for action in actions:
        print(action)


if __name__ == '__main__':
    main()
