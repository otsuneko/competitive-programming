import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

cur = 0
ini = 0
for i in range(N):
    cur += A[i]
    if cur < 0:
        ini = max(ini,-cur)

print(ini+cur)

# def is_ok(arg):
#     cur = arg
#     for i in range(N):
#         cur += A[i]
#         if cur < 0:
#             return False
#     return True

# def meguru_bisect(ng, ok):
#     while (abs(ok - ng) > 1):
#         mid = (ok + ng) // 2
#         if is_ok(mid):
#             ok = mid
#         else:
#             ng = mid
#     return ok

# cur = meguru_bisect(-1,10**18)
# for i in range(N):
#     cur += A[i]
# print(cur)