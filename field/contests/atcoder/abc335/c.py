import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

class Deque:
    def __init__(self, src_arr=[], max_size=300000):
        self.N = max(max_size, len(src_arr)) + 1
        self.buf = list(src_arr) + [None] * (self.N - len(src_arr))
        self.head = 0
        self.tail = len(src_arr)
    def __index(self, i):
        l = len(self)
        if not -l <= i < l: raise IndexError('index out of range: ' + str(i))
        if i < 0:
            i += l
        return (self.head + i) % self.N
    def __extend(self):
        ex = self.N - 1
        self.buf[self.tail+1 : self.tail+1] = [None] * ex
        self.N = len(self.buf)
        if self.head > 0:
            self.head += ex
    def is_full(self):
        return len(self) >= self.N - 1
    def is_empty(self):
        return len(self) == 0
    def append(self, x):
        if self.is_full(): self.__extend()
        self.buf[self.tail] = x
        self.tail += 1
        self.tail %= self.N
    def appendleft(self, x):
        if self.is_full(): self.__extend()
        self.buf[(self.head - 1) % self.N] = x
        self.head -= 1
        self.head %= self.N
    def pop(self):
        if self.is_empty(): raise IndexError('pop() when buffer is empty')
        ret = self.buf[(self.tail - 1) % self.N]
        self.tail -= 1
        self.tail %= self.N
        return ret
    def popleft(self):
        if self.is_empty(): raise IndexError('popleft() when buffer is empty')
        ret = self.buf[self.head]
        self.head += 1
        self.head %= self.N
        return ret
    def __len__(self):
        return (self.tail - self.head) % self.N
    def __getitem__(self, key):
        return self.buf[self.__index(key)]
    def __setitem__(self, key, value):
        self.buf[self.__index(key)] = value
    def __str__(self):
        return 'Deque({0})'.format(str(list(self)))

N,Q = map(int,input().split())

from collections import deque

parts = Deque([[i,0] for i in range(1,N+1)])

DIR = {"U":(1,0), "R":(0,1), "D":(-1,0), "L":(0,-1)}
for _ in range(Q):
    query = list(map(str,input().split()))
    if query[0] == "1":
        C = query[1]
        x,y = parts[0]
        ny,nx = y+DIR[C][0], x+DIR[C][1]
        parts.pop()
        parts.appendleft([nx,ny])
    else:
        p = int(query[1])
        print(*parts[p-1])