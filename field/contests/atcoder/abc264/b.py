R,C = map(int,input().split())
R,C = R-1,C-1
grid = ["bbbbbbbbbbbbbbb",
        "bwwwwwwwwwwwwwb",
        "bwbbbbbbbbbbbwb",
        "bwbwwwwwwwwwbwb",
        "bwbwbbbbbbbwbwb",
        "bwbwbwwwwwbwbwb",
        "bwbwbwbbbwbwbwb",
        "bwbwbwbwbwbwbwb",
        ]

if R >= 7:
    R = 7 - (R-7)

if grid[R][C] == "w":
    print("white")
else:
    print("black")