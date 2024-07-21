import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, TypeVar, Union, List
T = TypeVar('T')

class SortedSet(Generic[T]):
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None) -> None:
        "Evenly divide `a` into buckets."
        if a is None: a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [a[size * i // bucket_size : size * (i + 1) // bucket_size] for i in range(bucket_size)]

    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
        a = list(a)
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(set(a))
        self._build(a)

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i: yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i): yield j

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "SortedSet" + str(self.a)

    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _find_bucket(self, x: T) -> List[T]:
        "Find the bucket which should contain x. self must not be empty."
        for a in self.a:
            if x <= a[-1]: return a
        return a

    def __contains__(self, x: T) -> bool:
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x

    def add(self, x: T) -> bool:
        "Add an element and return True if added. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x: return False
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
        return True

    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x: return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0: self._build()
        return True

    def lt(self, x: T) -> Union[T, None]:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> Union[T, None]:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> Union[T, None]:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> Union[T, None]:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, x: int) -> T:
        "Return the x-th element, or IndexError if it doesn't exist."
        if x < 0: x += self.size
        if x < 0: raise IndexError
        for a in self.a:
            if x < len(a): return a[x]
            x -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans

H,W,Y = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

height = SortedSet()
for y in range(H):
    for x in range(W):
        height.add(A[y][x])

# 引数となるリストはソート不要かつ値の重複可(内部処理で対応するため)
def compress(arr):
    *XS, = set(arr)
    XS.sort()
    return {e: i for i, e in enumerate(XS)}

from collections import defaultdict
comp_height = compress(height)
comp_pos = defaultdict(list)

for y in range(H):
    for x in range(W):
        comp_pos[comp_height[A[y][x]]].append((y,x))

from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs_MultiStart(s,h):
    global field_cnt
    queue = deque(s)

    while queue:
        for _ in range(len(queue)):
            y,x = queue.popleft()
            if A[y][x] == 0:
                continue
            A[y][x] = 0
            field_cnt -= 1
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and A[ny][nx] <= h:
                    queue.append((ny, nx))

def is_near_sea(y,x,h):
    for dy,dx in MOVE:
        ny,nx = y+dy,x+dx
        if (ny in [-1,H] or nx in [-1,W]) and A[y][x] <= h:
            return True
        elif 0<=ny<H and 0<=nx<W and A[ny][nx] == 0:
            return True
    return False

field_cnt = H*W
last_field_cnt = H*W
last_year = 0
print_cnt = 0
for h in height:
    cand_pos = []
    for y,x in comp_pos[comp_height[h]]:
        if A[y][x] != 0 and is_near_sea(y,x,h):
            cand_pos.append((y,x))

    # 次に沈む高さのマスを起点に多始点BFS
    bfs_MultiStart(cand_pos,h)

    if h <= Y:
        for i in range(last_year+1, h):
            print(last_field_cnt)
            print_cnt += 1
        print(field_cnt)
        print_cnt += 1
    else:
        break

    last_year = h
    last_field_cnt = field_cnt

for i in range(print_cnt+1, Y+1):
    print(field_cnt)
