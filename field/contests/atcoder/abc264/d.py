class Bit:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)
  
    def sum(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s
  
    def add(self, i, x):
        while i <= self.size:
            self.tree[i] += x
            i += i & -i
 
S = list(input())
dict = {"a":1,"t":2,"c":3,"o":4,"d":5,"e":6,"r":7}

S2 = []
for s in S:
    S2.append(dict[s])

bit = Bit(16)
ans = 0
for i, p in enumerate(S2):
    ans += i - bit.sum(p)
    bit.add(p, 1)
 
print(ans)
