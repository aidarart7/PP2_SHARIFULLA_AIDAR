def g1(n):
    for i in range(1, n + 1):
        yield i * i
n = int(input())
for value in g1(n):
    print(value)

def g2(q):
    for i in range(0, q + 1, 2):
        yield i
q = int(input())
first = True
for value in g2(q):
    if not first:
        print(",", end="")
    print(value, end="")
    first = False
print()
def g3(w):
    for i in range(0, w + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
w = int(input())
first = True
for value in g3(w):
    if not first:
        print(" ", end="")
    print(value, end="")
    first = False         
print()

def g4(a,b):
    for i in range(a, b + 1):
        yield i * i
a, b = map(int, input().split())
for value in g4(a,b):
    print(value)       

def g5(s):
    for i in range(s, -1, -1):
        yield i
s = int(input())
for value in g5(s):
    print(value)