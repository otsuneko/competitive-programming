def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ (x,i) for i, x in enumerate(arr)], reverse=True, key=lambda x:(x[0],-x[1]))
    else:
        return sorted([ (x,i) for i, x in enumerate(arr)])

N,X,Y,Z = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
C = [a+b for a,b in zip(A,B)]

ans = []
check = set()
A2 = sort_with_index(A,reverse=True)
for i in range(X):
    ans.append(A2[i][1])
    check.add(A2[i][1])

B2 = sort_with_index(B,reverse=True)
y = idx = 0
while y < Y:
    if B2[idx][1] not in check:
        ans.append(B2[idx][1])
        check.add(B2[idx][1])
        y += 1
    idx += 1

C2 = sort_with_index(C,reverse=True)
z = idx = 0
while z < Z:
    if C2[idx][1] not in check:
        ans.append(C2[idx][1])
        check.add(C2[idx][1])
        z += 1
    idx += 1

ans.sort()
for a in ans:
    print(a+1)