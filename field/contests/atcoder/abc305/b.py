p,q = map(str,input().split())
S = "A--BC---DE----F--------G"
print(abs(S.index(q)-S.index(p)))