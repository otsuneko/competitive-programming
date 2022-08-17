S = [">"] + list(input()) + ["<"]

edge = []
for i in range(len(S)-1):
    if [S[i],S[i+1]] == [">","<"]:
        edge.append((i,"bottom"))
    elif [S[i],S[i+1]] == ["<",">"]:
        edge.append((i,"top"))
print(edge)

max_gap = 0
for i in range(len(edge)-1):
    max_gap = max(max_gap, abs(edge[i+1][0]-edge[i][0]))

print(max_gap)

ans = 0
for i in range(len(edge)-1):
    if edge[i][1] == "bottom":
        n = min(max_gap,edge[i+1][0]-edge[i][0])
        if n > 1:
            ans += n*(n-1)//2
    else:
        n = min(max_gap,edge[i+1][0]-edge[i][0])
        if n > 1:
            ans += n*(n+1)//2
print(ans)