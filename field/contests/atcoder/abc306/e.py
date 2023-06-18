# import sys
# input = sys.stdin.readline
# # https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
# import math
# from bisect import bisect_left, bisect_right, insort
# from typing import Generic, Iterable, Iterator, TypeVar, Union, List
# T = TypeVar('T')

# class SortedMultiset(Generic[T]):
#     BUCKET_RATIO = 50
#     REBUILD_RATIO = 170

#     def _build(self, a=None) -> None:
#         "Evenly divide `a` into buckets."
#         if a is None: a = list(self)
#         size = self.size = len(a)
#         bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
#         self.a = [a[size * i // bucket_size : size * (i + 1) // bucket_size] for i in range(bucket_size)]
    
#     def __init__(self, a: Iterable[T] = []) -> None:
#         "Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"
#         a = list(a)
#         if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
#             a = sorted(a)
#         self._build(a)

#     def __iter__(self) -> Iterator[T]:
#         for i in self.a:
#             for j in i: yield j

#     def __reversed__(self) -> Iterator[T]:
#         for i in reversed(self.a):
#             for j in reversed(i): yield j
    
#     def __len__(self) -> int:
#         return self.size
    
#     def __repr__(self) -> str:
#         return "SortedMultiset" + str(self.a)
    
#     def __str__(self) -> str:
#         s = str(list(self))
#         return "{" + s[1 : len(s) - 1] + "}"

#     def _find_bucket(self, x: T) -> List[T]:
#         "Find the bucket which should contain x. self must not be empty."
#         for a in self.a:
#             if x <= a[-1]: return a
#         return a

#     def __contains__(self, x: T) -> bool:
#         if self.size == 0: return False
#         a = self._find_bucket(x)
#         i = bisect_left(a, x)
#         return i != len(a) and a[i] == x

#     def count(self, x: T) -> int:
#         "Count the number of x."
#         return self.index_right(x) - self.index(x)

#     def add(self, x: T) -> None:
#         "Add an element. / O(√N)"
#         if self.size == 0:
#             self.a = [[x]]
#             self.size = 1
#             return
#         a = self._find_bucket(x)
#         insort(a, x)
#         self.size += 1
#         if len(a) > len(self.a) * self.REBUILD_RATIO:
#             self._build()

#     def discard(self, x: T) -> bool:
#         "Remove an element and return True if removed. / O(√N)"
#         if self.size == 0: return False
#         a = self._find_bucket(x)
#         i = bisect_left(a, x)
#         if i == len(a) or a[i] != x: return False
#         a.pop(i)
#         self.size -= 1
#         if len(a) == 0: self._build()
#         return True

#     def lt(self, x: T) -> Union[T, None]:
#         "Find the largest element < x, or None if it doesn't exist."
#         for a in reversed(self.a):
#             if a[0] < x:
#                 return a[bisect_left(a, x) - 1]

#     def le(self, x: T) -> Union[T, None]:
#         "Find the largest element <= x, or None if it doesn't exist."
#         for a in reversed(self.a):
#             if a[0] <= x:
#                 return a[bisect_right(a, x) - 1]

#     def gt(self, x: T) -> Union[T, None]:
#         "Find the smallest element > x, or None if it doesn't exist."
#         for a in self.a:
#             if a[-1] > x:
#                 return a[bisect_right(a, x)]

#     def ge(self, x: T) -> Union[T, None]:
#         "Find the smallest element >= x, or None if it doesn't exist."
#         for a in self.a:
#             if a[-1] >= x:
#                 return a[bisect_left(a, x)]
    
#     def __getitem__(self, x: int) -> T:
#         "Return the x-th element, or IndexError if it doesn't exist."
#         if x < 0: x += self.size
#         if x < 0: raise IndexError
#         for a in self.a:
#             if x < len(a): return a[x]
#             x -= len(a)
#         raise IndexError

#     def index(self, x: T) -> int:
#         "Count the number of elements < x."
#         ans = 0
#         for a in self.a:
#             if a[-1] >= x:
#                 return ans + bisect_left(a, x)
#             ans += len(a)
#         return ans

#     def index_right(self, x: T) -> int:
#         "Count the number of elements <= x."
#         ans = 0
#         for a in self.a:
#             if a[-1] > x:
#                 return ans + bisect_right(a, x)
#             ans += len(a)
#         return ans

# N,K,Q = map(int,input().split())

# A = [0]*N
# sms1 = SortedMultiset([0]*K)
# sms2 = SortedMultiset([0]*(N-K))
# ans = 0
# for _ in range(Q):
#     x,y = map(int,input().split())
#     x -= 1

#     old = A[x]
#     new = y
#     A[x] = new

#     # add
#     sms2.add(new)
#     # balance
#     while len(sms1) < K:
#         tmp = sms2[0]
#         sms2.discard(tmp)
#         sms1.add(tmp)
#         ans += tmp
#     while len(sms2) > 0 and sms1[0] < sms2[len(sms2)-1]:
#         tmp1,tmp2 = sms1[0],sms2[len(sms2)-1]
#         sms1.discard(tmp1)
#         sms2.discard(tmp2)
#         sms1.add(tmp2)
#         sms2.add(tmp1)
#         ans += tmp2-tmp1

#     # erase
#     if old in sms1:
#         sms1.discard(old)
#         ans -= old
#     else:
#         sms2.discard(old)
#     # balance
#     while len(sms1) < K:
#         tmp = sms2[0]
#         sms2.discard(tmp)
#         sms1.add(tmp)
#         ans += tmp
#     while len(sms2) > 0 and sms1[0] < sms2[len(sms2)-1]:
#         tmp1,tmp2 = sms1[0],sms2[len(sms2)-1]
#         sms1.discard(tmp1)
#         sms2.discard(tmp2)
#         sms1.add(tmp2)
#         sms2.add(tmp1)
#         ans += tmp2-tmp1
    
#     print(ans)

# convexineqさんの解答
# https://atcoder.jp/contests/abc306/submissions/42338907
# 値を指定しての削除可能heapq
from heapq import *
class DeletableHeapq:
    def __init__(self, initial = []):
        if initial:
            self.q = initial
            heapify(self.q)
        else:
            self.q = []
        self.q_del = []

    def propagate(self):
        while self.q_del and self.q[0] == self.q_del[0]:
            heappop(self.q)
            heappop(self.q_del)

    def heappop(self):
        self.propagate()
        return heappop(self.q)
    
    def __len__(self):
        return len(self.q) - len(self.q_del)        

    def top(self):
        self.propagate()
        return self.q[0]
            
    def remove(self,x):
        heappush(self.q_del,x)

    def heappush(self,x):
        heappush(self.q,x)

# リストを降順に見た際の上位K個の和を計算
class SumOfTopK:
    def __init__(self, K, initial = []):
        #assert len(initial) <= K
        self.K = K
        self.val = sum(initial)
        initial.sort()
        self.q_topK = DeletableHeapq(initial[:K])
        self.q_other = DeletableHeapq(initial[K:])

    # 上位K個の和を取得
    def getSum(self):
        return self.val

    # 値vを追加
    def add(self,v):
        self.q_topK.heappush(v)
        self.val += v
        if len(self.q_topK) == self.K+1:
            x = self.q_topK.heappop()
            self.val -= x
            self.q_other.heappush(-x)

    # 値vを削除
    def remove(self,v):
        t = self.q_topK.top()
        if t <= v:
            self.q_topK.remove(v)
            self.val -= v
            if len(self.q_other):
                x = -self.q_other.heappop()
                self.val += x
                self.q_topK.heappush(x)
        else:
            self.q_other.remove(-v)


import sys
readline = sys.stdin.readline

N,K,Q = map(int,readline().split())
A = [0]*N

hq = SumOfTopK(K,A)
for _ in range(Q):
    x,y = map(int,input().split())
    x -= 1

    hq.remove(A[x])
    A[x] = y
    hq.add(y)
    print(hq.getSum())
























# hq = SumOfTopK(K,A)
# for _ in range(Q):
#     x,y = map(int,readline().split())
#     x -= 1
#     hq.remove(A[x])
#     A[x] = y
#     hq.add(y)
#     print(hq.get())
