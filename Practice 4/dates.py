from datetime import date, datetime, timedelta
t = date.today()
n = t - timedelta(days=5)
print(n)

y = t - timedelta(days=1)
tw = t + timedelta(days=1)
print(y)
print(t)
print(tw)

q = datetime.now()
w = q.replace(microsecond=0)
print(w)

d1 = datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")
d = d2 - d1
print(d.total_seconds())