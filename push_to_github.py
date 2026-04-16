#!/usr/bin/env python3
"""
Push repository to GitHub
Usage: python push_to_github.py <REPO_URL>
Example: python push_to_github.py https://github.com/bhoomi/ear-disease-app.git
"""
import subprocess
import sys
import os

if len(sys.argv) < 2:
    print("❌ Error: Repository URL required!")
    print("\nUsage: python push_to_github.py <REPO_URL>")
    print("Example: python push_to_github.py https://github.com/bhoomi/ear-disease-app.git")
    sys.exit(1)

repo_url = sys.argv[1]
os.chdir(r'c:\Users\sheru\ear-disease-app')

# Git path
GIT = r'C:\Program Files\Git\bin\git.exe'

print(f"Adding remote origin: {repo_url}")
subprocess.run([GIT, 'remote', 'add', 'origin', repo_url], check=True)

print("Pushing to GitHub...")
subprocess.run([GIT, 'push', '-u', 'origin', 'main'], check=True)

print("\n✅ Successfully pushed to GitHub!")
print(f"\n📌 Your repository is live at: {repo_url.replace('.git', '')}")
