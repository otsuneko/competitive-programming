import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# 10進数⇒n進数
def base10int(value, base):
    if value >= base:
        return base10int(value//base, base) + str(value % base)
    return str(value % base)

N = int(input())

base5 = base10int(N-1,5)
ans = ""
for b in base5:
    ans += str(int(b)*2)
print(ans)


# base = [0,2,4,6,8]
# li = [0,2,4,6,8]
# cur = 1
# while 1:
#     print(li)
#     cnt = 0
#     for i in range(cur,len(li),1):
#         for b in base:
#             new = str(i) + str(b)
#             li.append(int(new))
#             cnt += 1
#             if len(li) > 10**12:
#                 break
#     cur += cnt

# print(li[N-1])