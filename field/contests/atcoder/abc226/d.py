from fractions import Fraction

N = int(input())
pos = [list(map(int,input().split())) for _ in range(N)]

magic = set()
for x1,y1 in pos:
    for x2,y2 in pos:
        if [x1,y1] == [x2,y2]:
            continue
        if x2-x1 == 0:
            if y2-y1 > 0:
                magic.add((1,0))
            else:
                magic.add((-1,0))
        else:
            frac = Fraction(y2-y1,x2-x1)
            magic.add((frac.numerator, frac.denominator))
            magic.add((-frac.numerator, -frac.denominator))


# print(magic)
print(len(magic))