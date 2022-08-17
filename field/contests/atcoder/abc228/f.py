H,W,h1,w1,h2,w2 = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

cumsum = [[0]*(W+1) for _ in range(H+1)]
for y in range(H):
    for x in range(W):
        cumsum[y+1][x+1] = cumsum[y][x+1] + cumsum[y+1][x] - cumsum[y][x] + A[y][x]

t_score = []
a_score = []
for y in range(H):
    for x in range(W):
        if y+h1 <= H and x+w1 <= W:
            t_score.append((cumsum[y+h1][x+w1]-cumsum[y+h1][x]-cumsum[y][x+w1], y,x))
        if y+h2 <= H and x+w2 <= W:
            a_score.append((cumsum[y+h2][x+w2]-cumsum[y+h2][x]-cumsum[y][x+w2], y,x))

t_score.sort(revrse=True)
t_y,t_x = t_score[0][1],t_score[0][2]
ans = 0
for y in range(H):
    for x in range(W):
        score = t_score[0][0]
        print(score)
        for dy in range(h2):
            for dx in range(w2):
                if t_y <= y+dy < t_y+h1 and t_x <= x+dx < t_x+w1:
                    score -= A[y+dy][x+dx]
        ans = max(ans,score)
print(ans)

# print(*cumsum, sep="\n")
# print(t_score)
# print(a_score)
# print(cumsum[H][W]-cumsum[1][1])
