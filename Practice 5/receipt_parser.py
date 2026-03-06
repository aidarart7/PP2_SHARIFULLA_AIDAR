import re

with open(r"C:\Users\LENOVO\Documents\PP2\Practice 5\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("TEXT LOADED\n")

p1 = r"ab*"
print("1:", re.findall(p1, text))


p2 = r"ab{2,3}"
print("2:", re.findall(p2, text))


p3 = r"[a-z]+_[a-z]+"
print("3:", re.findall(p3, text))


p4 = r"[A-Z][a-z]+"
print("4:", re.findall(p4, text))


p5 = r"a.*b"
print("5:", re.findall(p5, text))


r6 = re.sub(r"[ ,\.]", ":", text)
print("\n6 (first 200 chars):")
print(r6[:200])


def snake_to_camel(match):
    return match.group(1).upper()

r7 = re.sub(r"_([a-z])", snake_to_camel, text)
print("\n7 (first 200 chars):")
print(r7[:200])


r8 = re.findall(r"[A-Z][^A-Z]*", text)
print("\n8:", r8[:10])


r9 = re.sub(r"([A-Z])", r" \1", text)
print("\n9 (first 200 chars):")
print(r9[:200])


r10 = re.sub(r"([A-Z])", r"_\1", text).lower()
print("\n10 (first 200 chars):")
print(r10[:200])