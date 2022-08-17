import itertools
S = input()

certain = set([])
possible = set([])
for i in range(10):
    if S[i] == "o":
        certain.add(i)
    elif S[i] == "x":
        continue
    else:
        possible.add(i)

all = set([i for i in range(10)])
cmb = itertools.product(all,repeat=4)

ans = 0
for c in cmb:
    s = set(c)
    if certain & s != certain:
        continue
    if s & all-certain-possible != set([]):
        continue
    ans += 1
print(ans)    


### original code ###
# import itertools
# from collections import Counter
# S = input()

# certain = []
# possible = []
# for i in range(10):
#     if S[i] == "o":
#         certain.append(i)
#     elif S[i] == "x":
#         continue
#     else:
#         possible.append(i)

# ans = 0
# if len(certain) > 4 or len(certain)+len(possible) == 0:
#     ans = 0
# elif len(certain) == 4:
#     ans = 24
# else:
#     for i in range(4-len(certain)+1):
#         ptrn1 = itertools.combinations_with_replacement(certain, 4-len(certain)-i)
#         for p1 in ptrn1:
#             ptrn2 = itertools.combinations_with_replacement(possible, i)
#             for p2 in ptrn2:
#                 ptrn = [*certain,*p1,*p2]
#                 d = Counter(ptrn)
#                 add = 24
#                 for key in d:
#                     if d[key] == 2:
#                         add //= 2
#                     elif d[key] == 3:
#                         add //= 6
#                     elif d[key] == 4:
#                         add //= 24
#                 ans += add
# print(ans)
