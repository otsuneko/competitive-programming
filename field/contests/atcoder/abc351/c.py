import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N =  int(input())
A =  list(map(int,input().split()))

li = []

for a in A:
    li.append(a)
    while 1:
        if len(li) <= 1:
            break
        if li[-1] != li[-2]:
            break
        add = li[-1]+1
        li.pop()
        li.pop()
        li.append(add)

print(len(li))
