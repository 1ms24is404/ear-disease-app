#!/usr/bin/env python
"""
Quick launcher script for the Ear Disease Classification System
Run this script to start the web application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if essential requirements are met"""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8+ required")
        return False
    
    # Check if Flask is installed
    try:
        import flask
        print(f"✓ Flask {flask.__version__} is installed")
    except ImportError:
        print("✗ Flask not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    # Check if uploads directory exists
    uploads_dir = Path('app/static/uploads')
    if not uploads_dir.exists():
        uploads_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created uploads directory")
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("Ear Disease Classification System - Web Application")
    print("=" * 60)
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n✗ Setup incomplete. Please install dependencies:")
        print("  python -m pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("Starting application...")
    print("-" * 60)
    
    # Run the Flask app
    try:
        print()
        print("✓ Application started successfully!")
        print()
        print("📍 URL: http://127.0.0.1:5000")
        print("📍 Open in your browser to access the application")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        print()
        
        # Import and run the app
        from app import create_app
        flask_app = create_app()
        flask_app.run(debug=True, host='127.0.0.1', port=5000)
        
    except ImportError:
        # Fallback: run app.py directly
        print()
        import app as main_app
        print("Running application...")

if __name__ == '__main__':
    main()
