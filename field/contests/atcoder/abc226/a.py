X = input()
idx = X.index(".")
if int(X[idx+1]) >= 5:
    print(int(X[:idx])+1)
else:
    print(int(X[:idx]))