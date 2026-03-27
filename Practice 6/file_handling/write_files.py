with open("aaa.txt", "w") as f:
    f.write("First line\n")
    f.write("Second line\n")

with open("aaa.txt", "a") as f:
    f.write("Appended line\n")

print("Write + append done")