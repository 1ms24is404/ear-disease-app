#!/usr/bin/env python3
"""
Setup git repository and push to GitHub
"""
import subprocess
import os

os.chdir(r'c:\Users\sheru\ear-disease-app')

# Git path
GIT = r'C:\Program Files\Git\bin\git.exe'

# Initialize repository
print("Initializing git repository...")
subprocess.run([GIT, 'init'], check=True)

# Configure git
print("Configuring git user...")
subprocess.run([GIT, 'config', 'user.name', 'bhoomi'], check=True)
subprocess.run([GIT, 'config', 'user.email', '1ms24is404@msrit.edu'], check=True)

# Add all files
print("Adding files to git...")
subprocess.run([GIT, 'add', '.'], check=True)

# Commit
print("Creating initial commit...")
subprocess.run([GIT, 'commit', '-m', 'Initial commit: Multimodal Ear Disease Classification Web App'], check=True)

# Rename branch to main
print("Renaming branch to main...")
subprocess.run([GIT, 'branch', '-M', 'main'], check=True)

print("\n✅ Git repository initialized successfully!")
print("\nNext steps:")
print("1. Go to https://github.com/new")
print("2. Create a repository named 'ear-disease-app'")
print("3. Copy your repository URL (HTTPS)")
print("4. Run this command:")
print("   python push_to_github.py <YOUR_REPO_URL>")
print("\nExample:")
print("   python push_to_github.py https://github.com/bhoomi/ear-disease-app.git")
