import sys
sys.setrecursionlimit(10**7)

C = ["3","5","7"]
def dfs(li,flg):

    if len(li) > 9:
        return

    if all(flg):
        n = "".join(li)
        if int(n) <= N:
            s.add(n)

    for i,c in enumerate(C):
        li2 = li[:]
        li2.append(c)
        flg2 = flg[:]
        flg2[i] = True
        dfs(li2,flg2)

N = int(input())

s = set()
dfs([],[False,False,False])
print(len(s))