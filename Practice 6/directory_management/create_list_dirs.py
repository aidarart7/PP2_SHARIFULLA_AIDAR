import os

os.makedirs("test_dir/subdir", exist_ok=True)

print("Files:", os.listdir("."))
print("Current path:", os.getcwd())

files = os.listdir(".")
txt_files = [f for f in files if f.endswith(".txt")]

print("TXT files:", txt_files)