#!/usr/bin/env python3
# script to add random text as comments to python files in pull request

import os
import sys
import subprocess
import random
import glob

def get_changed_python_files():
    # get list of python files changed in this pull request
    try:
        result = subprocess.run(['git', 'diff', '--name-only', 'origin/main', 'HEAD'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        files = result.stdout.strip().split('\n')
        python_files = [f for f in files if f.endswith('.py') and os.path.exists(f)]
        return python_files
    except Exception:
        return []

def get_random_comment_file():
    # randomly select a text file from comment_possible folder
    comment_folder = "comment_possible"
    if not os.path.exists(comment_folder):
        return None
    
    text_files = glob.glob(os.path.join(comment_folder, "*.txt"))
    if not text_files:
        return None
    
    return random.choice(text_files)

def read_comment_content(file_path):
    # read content from comment file and format as comments
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # convert each line to a comment
        comment_lines = []
        for line in content.split('\n'):
            if line.strip():
                comment_lines.append(f"# {line.strip()}")
            else:
                comment_lines.append("#")
        
        return comment_lines
    except Exception:
        return []

def add_comment_to_file(file_path, comment_lines):
    # add comment lines to the bottom of a python file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # add comments at the end
        lines.append("\n")
        lines.append("# pylint: disable=useless-suppression\n")
        for comment_line in comment_lines:
            lines.append(comment_line + "\n")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True
    except Exception:
        return False

def commit_changes():
    # commit the changes to avoid recursive workflow triggers
    try:
        # configure git user
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
        
        # add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # commit with skip ci to prevent recursive triggers
        subprocess.run(['git', 'commit', '-m', 'add useless comments [skip ci]'], check=True)
        
        # push changes
        subprocess.run(['git', 'push'], check=True)
        
        return True
    except Exception as e:
        print(f"error committing changes: {e}")
        return False

def main():
    # main function to add random comments to changed python files
    changed_files = get_changed_python_files()
    if not changed_files:
        return 0
    
    # get random comment file
    comment_file = get_random_comment_file()
    if not comment_file:
        return 0
    
    # read comment content
    comment_lines = read_comment_content(comment_file)
    if not comment_lines:
        return 0
    
    # add comments to each changed python file
    modified_files = 0
    for file_path in changed_files:
        if add_comment_to_file(file_path, comment_lines):
            modified_files += 1
    
    # if files were modified, commit the changes
    if modified_files > 0:
        commit_changes()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
