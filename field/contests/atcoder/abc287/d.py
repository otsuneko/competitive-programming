S = list(input())
T = list(input())

ls = len(S)
lt = len(T)

front = [False]*(lt+1)
front[0] = True
end = [False]*(lt+1)
end[0] = True

for i in range(1,lt+1):
    if front[i-1] == True:
        if S[i-1] == T[i-1] or S[i-1] == "?" or T[i-1] == "?":
            front[i] = True
    else:
        break

for i in range(1,lt+1):
    if end[i-1] == True:
        if S[ls-i] == T[lt-i] or S[ls-i] == "?" or T[lt-i] == "?":
            end[i] = True
    else:
        break

# print(front,end)

for x in range(lt+1):
    print(["No","Yes"][front[x] and end[lt-x]])