H,W = map(int,input().split())
ans = []
ans.append(["#"*(W+2)])
for _ in range(H):
    tmp = list(input())
    ans.append(["#"] + tmp + ["#"])
ans.append(["#"*(W+2)])

for a in ans:
    print("".join(a))