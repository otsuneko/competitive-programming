from collections import Counter
S = input()
cnt = Counter(S)

if abs(cnt["a"]-cnt["b"]) <= 1 and abs(cnt["a"]-cnt["c"]) <= 1 and abs(cnt["c"]-cnt["b"]) <= 1:
    print("YES")
else:
    print("NO")