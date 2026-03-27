import shutil
import os

shutil.copy("aaa.txt", "bbb.txt")

if os.path.exists("bbb.txt"):
    os.remove("bbb.txt")
    print("File deleted")
else:
    print("File not found")