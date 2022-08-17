from collections import namedtuple
import math
import random

N = 16
M = 5000
T = 1000
MAX_DURATION = 20
DIV_V = 100

Vege = namedtuple('Vege', ['r', 'c', 's', 'e', 'v'])


class TestCase:

    def __init__(self, seed=None, input=None):
        if seed is not None:
            self.N = N
            self.M = M
            self.T = T
            self.veges = []
            random.seed(seed)
            pos = [[[] for _ in range(self.N)] for __ in range(self.N)]
            for i in range(self.M):
                while True:
                    duration = random.randrange(0, MAX_DURATION + 1)
                    s = random.randrange(0, self.T - 1 - duration + 1)
                    e = s + duration
                    r = random.randrange(0, N)
                    c = random.randrange(0, N)
                    if all(map(lambda v: v.e < s or e < v.s, pos[r][c])):
                        v = math.floor(pow(2.0, random.uniform(0.0, 1.0 + s / DIV_V)))
                        vege = Vege(r, c, s, e, v)
                        pos[r][c].append(vege)
                        self.veges.append(vege)
                        break
            self.veges.sort(key=lambda x: (x.s, x.r, x.c))
        else:
            itr = iter(input)
            self.N, self.M, self.T = map(int, next(itr).strip().split())
            self.veges = []
            for i in range(self.M):
                r, c, s, e, v = map(int, next(itr).split())
                self.veges.append(Vege(r, c, s, e, v))

    def __str__(self):
        ret = f"{self.N} {self.M} {self.T}\n"
        return ret + "\n".join(f"{v.r} {v.c} {v.s} {v.e} {v.v}" for v in self.veges)
