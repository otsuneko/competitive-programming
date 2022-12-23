class LazySegTree:
    def __init__(self, op, e, mapping, composition, id,
                 n: int = -1, v: list = []):
        assert (len(v) > 0) | (n > 0)
        if(len(v) == 0):
            v = [e()] * n
        self.__n = len(v)
        self.__log = (self.__n - 1).bit_length()
        self.__size = 1 << self.__log
        self.__d = [e()] * (2 * self.__size)
        self.__lz = [id()] * self.__size
        self.__op = op
        self.__e = e
        self.__mapping = mapping
        self.__composition = composition
        self.__id = id

        for i in range(self.__n):
            self.__d[self.__size + i] = v[i]
        for i in range(self.__size - 1, 0, -1):
            self.__update(i)

    def __update(self, k: int):
        self.__d[k] = self.__op(self.__d[2 * k], self.__d[2 * k + 1])

    def __all_apply(self, k: int, f):
        self.__d[k] = self.__mapping(f, self.__d[k])
        if(k < self.__size):
            self.__lz[k] = self.__composition(f, self.__lz[k])

    def __push(self, k: int):
        self.__all_apply(2*k, self.__lz[k])
        self.__all_apply(2*k+1, self.__lz[k])
        self.__lz[k] = self.__id()

    # 1点更新
    def set(self, p: int, x):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        self.__d[p] = x
        for i in range(1, self.__log + 1):
            self.__update(p >> i)

    # 1点取得
    def get(self, p: int):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        return self.__d[p]

    # 区間演算
    def prod(self, l: int, r: int):
        assert (0 <= l) & (l <= r) & (r <= self.__n)
        if(l == r):
            return self.__e()

        l += self.__size
        r += self.__size

        for i in range(self.__log, 0, -1):
            if((l >> i) << i) != l:
                self.__push(l >> i)
            if((r >> i) << i) != r:
                self.__push(r >> i)

        sml = self.__e()
        smr = self.__e()
        while(l < r):
            if(l & 1):
                sml = self.__op(sml, self.__d[l])
                l += 1
            if(r & 1):
                r -= 1
                smr = self.__op(self.__d[r], smr)
            l //= 2
            r //= 2

        return self.__op(sml, smr)

    # 全体演算
    def all_prod(self):
        return self.__d[1]

    # 1点写像
    def apply(self, p: int, f):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        self.__d[p] = self.__mapping(f, self.__d[p])
        for i in range(1, self.__log+1):
            self.__update(p >> i)

    # 区間写像
    def apply_lr(self, l: int, r: int, f):
        assert (0 <= l) & (l <= r) & (r <= self.__n)
        if(l == r):
            return

        l += self.__size
        r += self.__size

        for i in range(self.__log, 0, -1):
            if((l >> i) << i) != l:
                self.__push(l >> i)
            if((r >> i) << i) != r:
                self.__push((r-1) >> i)

        l2, r2 = l, r
        while(l < r):
            if(l & 1):
                self.__all_apply(l, f)
                l += 1
            if(r & 1):
                r -= 1
                self.__all_apply(r, f)
            l //= 2
            r //= 2
        l, r = l2, r2

        for i in range(1, self.__log+1):
            if((l >> i) << i) != l:
                self.__update(l >> i)
            if((r >> i) << i) != r:
                self.__update((r-1) >> i)

    # L固定時の最長区間のR
    def max_right(self, l: int, g):
        assert (0 <= l) & (l <= self.__n)
        assert g(self.__e())
        if(l == self.__n):
            return self.__n
        l += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(l >> i)
        sm = self.__e()
        while(True):
            while(l % 2 == 0):
                l //= 2
            if(not g(self.__op(sm, self.__d[l]))):
                while(l < self.__size):
                    self.__push(l)
                    l *= 2
                    if(g(self.__op(sm, self.__d[l]))):
                        sm = self.__op(sm, self.__d[l])
                        l += 1
                return l - self.__size
            sm = self.__op(sm, self.__d[l])
            l += 1
            if(l & -l) == l:
                break
        return self.__n

    # R固定時の最長区間のL
    def min_left(self, r: int, g):
        assert (0 <= r) & (r <= self.__n)
        assert g(self.__e())
        if(r == 0):
            return 0
        r += self.__size
        for i in range(self.__log, 0, -1):
            self.__push((r-1) >> i)
        sm = self.__e()
        while(True):
            r -= 1
            while(r > 1) & (r % 2):
                r //= 2
            if(not g(self.__op(self.__d[r], sm))):
                while(r < self.__size):
                    self.__push(r)
                    r = 2 * r + 1
                    if(g(self.__op(self.__d[r], sm))):
                        sm = self.__op(self.__d[r], sm)
                        r -= 1
                return r + 1 - self.__size
            sm = self.__op(self.__d[r], sm)
            if(r & -r) == r:
                break
        return 0

    def all_push(self):
        for i in range(1,self.__size):
            self.__push(i)

    def get_all(self):
        self.all_push()
        return self.__d[self.__size:self.__size+self.__n]

# ノード間演算(prodなど)
def op(s, t):
    return s + t

# opの恒等写像
def e():
    return 0
 
# 各ノードに対する更新作用(applyなど)
def mapping(f,x):
    return f^x

# f(g())の合成写像
def composition(f,g):
    return f^g

# mappingの恒等写像
def id():
    return 0

N,Q = map(int,input().split())
v = [0]*N

lst = LazySegTree(op=op,
                  e=e,
                  mapping=mapping,
                  composition=composition,
                  id=id,
                  v=v
                  )

# lst = LazySegTree(op=lambda x,y:0,
#                   e=lambda: 0,
#                   mapping=mapping,
#                   composition=composition,
#                   id=lambda: 0,
#                   v=v
#                   )

for _ in range(Q):
    l,r = map(int,input().split())
    l -= 1
    lst.apply_lr(l,r, 1)

ans = lst.get_all()
print(ans)
print(''.join(map(str,ans)))