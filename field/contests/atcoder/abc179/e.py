N,X,M = map(int,input().split())

li = [X]
loop_start = 0
check = set([X])
for i in range(N):
    nxt = pow(li[-1],2,M)
    if nxt in check:
        loop_start = li.index(nxt)
        break
    li.append(nxt)
    check.add(nxt)

loop_len = len(li)-loop_start
r = (N-loop_start)//loop_len
d = (N-loop_start)%loop_len
ini_sum = sum(li[:loop_start])
loop_sum = sum(li[loop_start:])*r
mod_sum = sum(li[loop_start:loop_start+d])
print(ini_sum + loop_sum + mod_sum)
