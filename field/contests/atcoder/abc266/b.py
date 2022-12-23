N = int(input())
mod = 998244353

print(N%mod)

# def is_ok(arg):
#     if mod*arg > N:
#         return True
#     else:
#         return False

# def meguru_bisect(ng, ok):
#     while (abs(ok - ng) > 1):
#         mid = (ok + ng) // 2
#         if is_ok(mid):
#             ok = mid
#         else:
#             ng = mid
#     return ok

# N = int(input())
# mod = 998244353

# k = meguru_bisect(-10**18,10**18)
# k -= 1
# # print(k)
# print(N-mod*k)
