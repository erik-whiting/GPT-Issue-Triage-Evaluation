import os


with open("list_of_files.txt") as fh:
    files = [f.strip() for f in fh.readlines()]

actual_files = []

for f in files:
    if os.path.exists(f):
        actual_files.append(f)


print(f"Found {len(actual_files)} files")
with open("actual_files", "w") as fh:
    fh.write("\n".join(actual_files))
