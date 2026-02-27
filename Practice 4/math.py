import math
d = float(input())
r = d * (math.pi / 180)
print(f"{r:.6f}")
q = math.radians(d)
print(f"{q:.6f}")

h = float(input())
a = float(input())
b = float(input())
at = ((a + b) / 2) * h
print(at)

n = int(input())
l = int(input())
arp = (n * l * l) /(4 * math.tan(math.pi / n))
print(arp)

aa = float(input())
hh = float(input())
ap = aa * hh
print(ap)