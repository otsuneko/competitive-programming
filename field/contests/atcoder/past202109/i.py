import bisect
from collections import deque
N = int(input())
A = list(map(int,input().split()))

even = []
odd = []
for a in A:
    if a%2:
        odd.append(a)
    else:
        even.append(a)

even = deque(sorted(even))
odd = deque(sorted(odd))

ans = min(A)
while even:
    n = even.pop()
    n //= 2
    # print(n,even,odd)
    if n%2:
        if even and odd:
            if n <= even[0] and n <= odd[0]:
                bisect.insort(odd,n*3)
            elif even[0] <= odd[0] and even[0] <= n:
                n2 = even.popleft()
                bisect.insort(even,n2*3)
                bisect.insort(odd,n)
            elif odd[0] <= even[0] and odd[0] <= n:
                n2 = odd.popleft()
                bisect.insort(odd,n2*3)
                bisect.insort(odd,n)
        elif odd:
            if n < odd[0]:
                bisect.insort(odd,n*3)
            else:
                n2 = odd.popleft()
                bisect.insort(odd,n2*3)
                bisect.insort(odd,n)
        elif even:
            if n < even[0]:
                bisect.insort(odd,n*3)
            else:
                n2 = even.popleft()
                bisect.insort(even,n2*3)
                bisect.insort(even,n)
        else:
            odd.append(n*3)
    else:
        if even and odd:
            if n <= even[0] and n <= odd[0]:
                bisect.insort(even,n*3)
            elif even[0] <= odd[0] and even[0] <= n:
                n2 = even.popleft()
                bisect.insort(even,n2*3)
                bisect.insort(even,n)
            elif odd[0] <= even[0] and odd[0] <= n:
                n2 = odd.popleft()
                bisect.insort(odd,n2*3)
                bisect.insort(even,n)
        elif odd:
            if n < odd[0]:
                bisect.insort(even,n*3)
            else:
                n2 = odd.popleft()
                bisect.insort(odd,n2*3)
                bisect.insort(even,n)
        elif even:
            if n < even[0]:
                bisect.insort(even,n*3)
            else:
                n2 = even.popleft()
                bisect.insort(even,n2*3)
                bisect.insort(even,n)
        else:
            even.append(n*3)

    if even and odd:
        ans = max(ans, min(even[0],odd[0]))
    elif odd:
        ans = max(ans, odd[0])
    elif even:
        ans = max(ans, even[0])

print(ans)