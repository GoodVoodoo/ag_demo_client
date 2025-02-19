import os
import subprocess
from pathlib import Path

def get_git_status():
    """Get git status in a more parseable format"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, 
                              text=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git is not installed")
        return []

def analyze_changes():
    changes = get_git_status()
    if not changes:
        print("No changes to commit")
        return

    modified = []
    new_files = []
    deleted = []

    for change in changes:
        status = change[:2]
        file_path = change[3:]
        
        if status == 'M ':
            modified.append(file_path)
        elif status == '??':
            new_files.append(file_path)
        elif status == 'D ':
            deleted.append(file_path)

    # Print summary
    print("\nGit Status Analysis:")
    print("===================")
    
    if modified:
        print("\nModified files:")
        for file in modified:
            print(f"  - {file}")
    
    if new_files:
        print("\nNew files:")
        for file in new_files:
            print(f"  - {file}")
    
    if deleted:
        print("\nDeleted files:")
        for file in deleted:
            print(f"  - {file}")

    # Suggest commit message
    if changes:
        print("\nSuggested commit actions:")
        if new_files:
            print(f"git add {' '.join(new_files)}")
        if modified or deleted:
            print(f"git add .")
        
        # Suggest commit message based on changes
        msg_parts = []
        if new_files:
            msg_parts.append(f"Add {len(new_files)} new file(s)")
        if modified:
            msg_parts.append(f"Update {len(modified)} file(s)")
        if deleted:
            msg_parts.append(f"Remove {len(deleted)} file(s)")
        
        commit_msg = " and ".join(msg_parts)
        print(f'git commit -m "{commit_msg}"')

if __name__ == "__main__":
    analyze_changes()  