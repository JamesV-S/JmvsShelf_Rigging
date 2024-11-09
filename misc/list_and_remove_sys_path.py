import sys

# Define the path you want to search for and remove
path_to_remove = r"E:\My_RIGGING/JmvsSCRIPTS/locator_file_imports/rev_loc_template.mb"

# Check if the path exists in sys.path
if path_to_remove in sys.path:
    #sys.path.remove(path_to_remove)
    print(f"To Remove: {path_to_remove}")
else:
    print(f"Path not found: {path_to_remove}")

# Optionally, print the updated sys.path to confirm
print("Updated sys.path:")
for p in sys.path:
    print(p)