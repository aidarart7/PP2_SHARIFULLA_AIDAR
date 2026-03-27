with open("aaa.txt", "r") as f:
    print("Full content:")
    print(f.read())

with open("aaa.txt", "r") as f:
    print("Line by line:")
    for line in f:
        print(line.strip())