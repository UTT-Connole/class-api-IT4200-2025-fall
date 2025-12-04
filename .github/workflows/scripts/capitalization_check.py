import os
import sys
import glob
from pathlib import Path
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
except ImportError:
    # Fallback if rich is not available
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    def rprint(*args, **kwargs):
        print(*args)

def find_python_files(root_dir="."):
    # Find all Python files in the repository.
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip common directories we don't want to check
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv'}]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def check_file_for_capitals(file_path):
    # Check a single Python file for any uppercase letters.
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Skip comment lines (lines that start with # after stripping whitespace)
            stripped_line = line.strip()
            if stripped_line.startswith('#'):
                continue
            
            # For lines with inline comments, only check the code part
            comment_pos = line.find('#')
            if comment_pos != -1:
                # Only check the part before the comment
                line_to_check = line[:comment_pos]
            else:
                line_to_check = line
            
            # Find all uppercase letters in the non-comment part of the line
            uppercase_chars = []
            for char_pos, char in enumerate(line_to_check):
                if char.isupper():
                    uppercase_chars.append((char_pos + 1, char))
            
            if uppercase_chars:
                violations.append({
                    'line': line_num,
                    'content': line.rstrip(),
                    'capitals': uppercase_chars
                })
    
    except Exception as e:
        print(f"error reading {file_path}: {e}")
        return []
    
    return violations

def main():
    print("Starting capitalization check...\n")
    # Main function to check all Python files for capitalization.
    console = Console()
    
    # Find all Python files
    python_files = find_python_files()
    
    if not python_files:
        return 0
    
    all_violations = {}
    total_violations = 0
    
    for file_path in python_files:
        violations = check_file_for_capitals(file_path)
        if violations:
            all_violations[file_path] = violations
            total_violations += len(violations)
    
    if all_violations:
        print(all_violations)
        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())