import os

def list_project_contents(directory_path):
    """
    Recursively lists all files and folders within your specific 
    Developer_Resource_Intelligence project.
    """
    # Converting to absolute path to ensure accuracy
    abs_path = os.path.abspath(directory_path)
    
    if not os.path.exists(abs_path):
        print(f"Error: The path {abs_path} was not found.")
        return

    print(f"--- Project Structure for: {abs_path} ---\n")
    
    for root, dirs, files in os.walk(abs_path):
        # Skip hidden folders like .pytest_cache or __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
        
        level = root.replace(abs_path, '').count(os.sep)
        indent = ' ' * 4 * level
        
        print(f"{indent}[Folder] {os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}[File] {f}")

if __name__ == "__main__":
    # Path integrated from your screenshot
    my_root = r"C:\Users\user\Desktop\Developer_Resource_Intelligence"
    
    list_project_contents(my_root)