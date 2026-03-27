import shutil
import os

os.makedirs("test_dir", exist_ok=True)

if os.path.exists("aaa.txt"):
    shutil.move("aaa.txt", "test_dir/aaa.txt")
    print("File moved")
else:
    print("aaa.txt not found")