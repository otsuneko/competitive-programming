N = int(input())
S = input()
T = input()

ans = True
for s,t in zip(S,T):
    if not (s == t or s in ["1","l"] and t in ["1","l"] or s in ["0","o"] and t in ["0", "o"]):
        ans = False
print(["No","Yes"][ans])