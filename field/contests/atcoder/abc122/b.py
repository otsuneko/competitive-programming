S = input()

ans = 0
cnt = 0
for c in S:
    if c in ["A","C","G","T"]:
        cnt += 1
    else:
        ans = max(ans,cnt)
        cnt = 0

print(max(ans,cnt))