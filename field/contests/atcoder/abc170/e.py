# 値の挿入、削除、最小値取得がO(logN)で可能なheapq
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

N,Q = map(int,input().split())

rate = [0]*N
place = [0]*N
kinder = [DeletableHeapq() for _ in range(2*10**5)]
top = DeletableHeapq()
tops = []

for i in range(N):
    a,b = map(int,input().split())
    b -= 1
    rate[i] = a
    place[i] = b
    kinder[b].heappush(-a)

for k in kinder:
    if k:
        top.heappush(-k.top())
        tops.append(k.top())
    else:
        tops.append(0)

for _ in range(Q):
    c,d = map(int,input().split())
    c,d = c-1,d-1
    r,p = rate[c], place[c]

    kinder[p].remove(-r)
    if not kinder[p]:
        tops[p] = 0
        top.remove(r)
    elif tops[p] != kinder[p].top():
        tops[p] = kinder[p].top()
        top.remove(r)
        top.heappush(-kinder[p].top())

    kinder[d].heappush(-r)
    if -r < tops[d]:
        top.remove(-tops[d])
        top.heappush(r)
        tops[d] = -r

    place[c] = d
    print(top.top())