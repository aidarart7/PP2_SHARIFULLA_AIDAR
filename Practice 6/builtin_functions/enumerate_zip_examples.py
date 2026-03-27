names = ["Aidar", "Alan", "Vladimir"]
scores = [90, 85, 88]

for i, name in enumerate(names):
    print(i, name)

for name, score in zip(names, scores):
    print(name, score)

x = "123"
print("Type of x:", type(x))

y = int(x)
print("Converted:", y, type(y))

a = 10
b = float(a)
print("Float:", b, type(b))