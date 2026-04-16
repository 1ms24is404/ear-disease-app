#!/usr/bin/env python
"""
Setup verification script for Ear Disease Classification System
Run this to verify your installation is complete and working.
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Error: Python 3.8+ required")
        return False
    return True

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        'app',
        'app/templates',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/uploads',
        'models'
    ]
    
    print("\nChecking directory structure...")
    all_exist = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_exist = False
    
    return all_exist

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'app/templates/index.html',
        'app/templates/help.html',
        'app/static/css/style.css',
        'app/static/js/main.js',
        'models/inference.py',
        'models/model_saver.py',
    ]
    
    print("\nChecking files...")
    all_exist = True
    for file_name in required_files:
        path = Path(file_name)
        if path.exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask',
        'torch',
        'torchvision',
        'timm',
        'sklearn',
        'pandas',
        'numpy',
        'PIL'
    ]
    
    print("\nChecking dependencies...")
    all_installed = True
    for package_name in required_packages:
        try:
            # Handle special cases
            if package_name == 'sklearn':
                importlib.import_module('sklearn')
            elif package_name == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_models():
    """Check if trained models exist"""
    model_files = [
        ('models/vit_ear_model.pth', 'ViT Model'),
        ('models/symptom_rf_model.pkl', 'Random Forest Model'),
    ]
    
    print("\nChecking trained models...")
    models_exist = False
    for file_path, description in model_files:
        path = Path(file_path)
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"  ✓ {description} ({size_mb:.2f} MB)")
            models_exist = True
        else:
            print(f"  ⚠ {description} - NOT FOUND (running in demo mode)")
    
    return models_exist

def check_permissions():
    """Check if write permissions exist for upload folder"""
    print("\nChecking permissions...")
    upload_dir = Path('app/static/uploads')
    
    if not upload_dir.exists():
        upload_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = upload_dir / '.test'
    try:
        test_file.touch()
        test_file.unlink()
        print(f"  ✓ Write permissions OK for {upload_dir}/")
        return True
    except Exception as e:
        print(f"  ✗ Permission denied for {upload_dir}/: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Ear Disease Classification System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_files),
        ("Dependencies", check_dependencies),
        ("Models", check_models),
        ("Permissions", check_permissions),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"✗ Error during {check_name} check: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print("\n" + "=" * 60)
    
    # Check if ready to run
    critical_checks = [
        "Python Version",
        "Directory Structure",
        "Required Files",
        "Dependencies",
        "Permissions"
    ]
    
    critical_passed = all(results.get(check, False) for check in critical_checks)
    models_found = results.get("Models", False)
    
    if critical_passed:
        print("✓ Setup is complete and ready to run!")
        if not models_found:
            print("\n⚠ Note: Trained models not found.")
            print("  The app will run in DEMO MODE with mock predictions.")
            print("  To use real predictions, copy trained models to:")
            print("    - models/vit_ear_model.pth")
            print("    - models/symptom_rf_model.pkl")
        print("\nTo start the application, run:")
        print("  python app.py")
    else:
        print("✗ Setup is incomplete. Please fix the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
