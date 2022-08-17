A,B,W = map(int,input().split())
W *= 1000

min_ans = 10**18
max_ans = 0
for i in range(1,10**6+1):
    if A*i <= W <= B*i:
        min_ans = min(min_ans, i)
        max_ans = max(max_ans, i)

if min_ans == 10**18 or max_ans == 0:
    print("UNSATISFIABLE")
else:
    print(min_ans, max_ans)
