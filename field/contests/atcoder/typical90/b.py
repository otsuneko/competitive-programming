import itertools
N = int(input())
if N%2:
    exit()

ans = 0
bit_list = list(itertools.product([0, 1], repeat=N))
for bits in bit_list:
    if bits.count(1) != len(bits)/2:
        continue
    cnt_0 = cnt_1 = 0
    ans = ""
    for b in bits:
        if b == 0:
            cnt_0 += 1
            ans += "("
        elif b == 1:
            cnt_1 += 1
            ans += ")"
        if cnt_1 > cnt_0:
            break
    else:
        print(ans)

# original answer
# N = int(input())
# if N%2:
#     exit()

# n_dict = {}
# n_dict[0] = set([""])
# n_dict[2] = set(["()"])
# for i in range(4,N+1,2):
#     s = set([])
#     target = i
#     for n in range(2,target//2+1,2):
#         for v in n_dict[n]:
#             for v2 in n_dict[target-n]:
#                 s.add(v+v2)
#                 s.add(v2+v)
#                 s.add("("*((target-n)//2)+v+")"*((target-n)//2))
#                 s.add("("*(n//2)+v2+")"*(n//2))
#     n_dict[target] = s

# ans = sorted(list(n_dict[N]))
# print(*ans, sep="\n")