# import sys
# sys.setrecursionlimit(10**7)

# def dfs(s,seen):

#     path.append(s)

#     if seen[s]:
#         return s,len(path)-1

#     seen[s] = True

#     return dfs(A[s-1],seen)

# N,K = map(int,input().split())
# A = list(map(int,input().split()))

# seen = [False]*(N+1)
# path = []
# n,end = dfs(1,seen)
# loop_start = path.index(n)
# if K < loop_start:
#     ans = path[K]
# else:
#     K -= loop_start
#     ans = path[loop_start + K%(end-loop_start)]
# print(ans)


# ダブリング解
# https://github.com/cozysauna/competitive-programming-python/blob/master/number/doubling.py
class Doubling:
    def __init__(self, A):
        self.logK = 60 # 2**60 > 10**18
        N = len(A)
        self.dbl = [[0] * N for _ in range(self.logK)]
        for i in range(N):
            self.dbl[0][i] = A[i]
        for k in range(self.logK-1):
            for i in range(N):
                self.dbl[k+1][i] = self.dbl[k][self.dbl[k][i]]
 
    # start -> A[start] -> A[A[start]] ... (loop times)
    def move(self, start, loop):
        now = start
        for k in range(self.logK):
            if loop >> k & 1: now = self.dbl[k][now]
        return now

N,K = map(int,input().split())
A = list(map(int,input().split()))
for i in range(N):
    A[i] -= 1

dbl = Doubling(A)
print(dbl.move(0,K)+1)
