from random import randrange
MOD = (1 << 61) - 1
BASE = randrange(2, MOD - 1) # Hash衝突攻撃対策
class RollingHash():
    def __init__(self, s):
        self.mod = MOD
        self.base = BASE
        self.pw = pw = [1] * (len(s) + 1)

        l = len(s)
        self.h = h = [0]*(l+1)

        v = 0
        for i in range(l):
            h[i+1] = v = (v * self.base + ord(s[i])) % self.mod
        v = 1
        for i in range(l):
            pw[i+1] = v = v * self.base % self.mod
    def get(self, l, r):
        return (self.h[r] - self.h[l] * self.pw[r-l]) % self.mod

N = int(input())
T = input()
T2 = T[:N] + T[N:][::-1]
Roll_T = RollingHash(T2)

for i in range(N):
    if Roll_T.get(0,i+1) == Roll_T.get(2*N-1-i,2*N) and Roll_T.get(i+1,N) == Roll_T.get(N,2*N-1-i):
        print(T[:i+1]+T[i+1:N][::-1])
        print(i+1)
        exit()
print(-1)
