from datetime import date, timedelta

def date_range(start, stop, step = timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step

y,m,d =map(int,input().split("/"))

for date in date_range(date(y, m, d), date(4000, 12, 31)):
    date = date.strftime("%Y/%m/%d")
    check = set()
    for c in str(date):
        check.add(c)
    if len(check) == 3:
        print(date)
        break