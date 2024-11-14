#!/usr/bin/env python3
import os
import shutil

def clean_pycache():
    """Remove all __pycache__ directories and .pyc files"""
    count = 0
    current_dir = os.getcwd()
    
    # Walk through all directories
    for root, dirs, files in os.walk(current_dir):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")
            count += 1
            
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                os.remove(pyc_file)
                print(f"Removed: {pyc_file}")
                count += 1

    if count == 0:
        print("No __pycache__ directories or .pyc files found.")
    else:
        print(f"\nTotal {count} items cleaned.")

if __name__ == "__main__":
    clean_pycache()