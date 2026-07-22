#!/usr/bin/env python3
"""
Test script to verify Python setup for milestones deck generation
"""

import sys
import importlib.util

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor}.{version.micro} is too old")
        print("   Required: Python 3.7 or higher")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} is not installed")
        return False
    else:
        print(f"✅ {package_name} is installed")
        return True

def main():
    print("Python Setup Test for Milestones Deck Generator")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check required packages
    packages = ['pptx']
    packages_ok = all(check_package(pkg) for pkg in packages)
    
    print()
    if python_ok and packages_ok:
        print("✅ All checks passed!")
        print("\nTo generate the milestones deck:")
        print("1. Run: pip install -r requirements-pptx.txt")
        print("2. Run: python scripts/generate-milestones-deck.py")
        print("3. Or run: generate-deck-python.bat (Windows)")
        print("4. Or run: .\\generate-deck-python.ps1 (PowerShell)")
        return 0
    else:
        print("❌ Some checks failed")
        print("\nPlease install missing dependencies:")
        print("1. Install Python 3.7+ from https://python.org/")
        print("2. Run: pip install -r requirements-pptx.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())