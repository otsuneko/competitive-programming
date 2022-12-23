T =int(input())

for _ in range(T):
    a,s =map(int,input().split())
    
    if s >= 2*a and s-2*a & a == 0:
        print("Yes")
    else:
        print("No")

# # 10進数⇒2,8,16進数
# x = 10
# bin_x = bin(x)[2:]
# oct_x = oct(x)[2:]
# hex_x = hex(x)[2:]

# T =int(input())

# for _ in range(T):
#     a,s =map(int,input().split())

#     #x AND s-x == aが存在するか    
#     ba = bin(a)[2:]
#     bs = bin(s)[2:]
#     l = max(len(ba),len(bs))
#     ba = str(ba).zfill(l)
#     bs = str(bs).zfill(l)
#     x = []
#     invx = []
#     for i in range(l):
#         if ba[i] == "1":
#             x.append("1")
#             invx.append("0")
#         else:
#             x.append("0")
#             invx.append("1")
#     x = "".join(x)
#     invx = "".join(invx)
#     invx = str(bin(int(x,2)+1)[2:])

#     # print(bs,x,ba)

#     carry = 0
#     bsx = []
#     ans = "No"
#     for i in range(l-1,-1,-1):
#         if bs[i] == "0" and invx[i] == "1":
#             if carry:
#                 carry = 1
#                 bsx.append("0")
#             else:
#                 bsx.append("1")
#         elif bs[i] == "0" and invx[i] == "0":
#             if carry:
#                 carry = 0
#                 bsx.append("1")
#             else:
#                 bsx.append("0")
#         elif bs[i] == "1" and invx[i] == "0":
#             if carry:
#                 carry = 1
#                 bsx.append("0")
#             else:
#                 bsx.append("1")
#         elif bs[i] == "1" and invx[i] == "1":
#             if carry:
#                 bsx.append("1")
#             else:
#                 carry = 1
#                 bsx.append("0")
#     sx = "".join(bsx)[::-1]
#     print(x,sx)

#     if int(x,2) > 0 and int(sx,2) > 0:
#         ans = "Yes"
#     else:
#         ans = "No"
#     print(ans)