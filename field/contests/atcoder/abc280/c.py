S = input()
T = input()

for i,(s,t) in enumerate(zip(S,T)):
    if s != t:
        print(i+1)
        break
else:
    print(len(S)+1)