#!/usr/bin/env python3
"""
Verification script for milestones deck generation setup
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status"""
    if os.path.exists(file_path):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - MISSING")
        return False

def main():
    print("Milestones Deck Setup Verification")
    print("=" * 50)
    
    # Get the project root
    project_root = Path(__file__).parent.parent
    
    # Files to check
    files_to_check = [
        # Node.js files
        (project_root / "package.json", "Node.js package.json"),
        (project_root / "scripts" / "generate-milestones-deck.js", "Node.js generation script"),
        (project_root / "scripts" / "test-setup.js", "Node.js test script"),
        (project_root / "generate-deck.bat", "Windows batch file (Node.js)"),
        (project_root / "generate-deck.ps1", "PowerShell script (Node.js)"),
        
        # Python files
        (project_root / "requirements-pptx.txt", "Python requirements file"),
        (project_root / "scripts" / "generate-milestones-deck.py", "Python generation script"),
        (project_root / "scripts" / "test-setup-python.py", "Python test script"),
        (project_root / "generate-deck-python.bat", "Windows batch file (Python)"),
        (project_root / "generate-deck-python.ps1", "PowerShell script (Python)"),
        
        # Documentation
        (project_root / "README-milestones-deck.md", "Main documentation"),
        (project_root / "scripts" / "README.md", "Scripts directory documentation"),
        (project_root / "test-setup-python.bat", "Python test batch file"),
    ]
    
    # Check files
    all_files_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    print()
    
    # Check directories
    directories_to_check = [
        (project_root / "docs", "Documentation directory"),
        (project_root / "scripts", "Scripts directory"),
    ]
    
    for dir_path, description in directories_to_check:
        if dir_path.exists():
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MISSING")
            all_files_exist = False
    
    print()
    
    # Summary
    if all_files_exist:
        print("✅ All files and directories are in place!")
        print("\nTo generate the milestones deck:")
        print("1. Choose Node.js or Python (see README-milestones-deck.md)")
        print("2. Run the appropriate generation script")
        print("3. The presentation will be created at: docs/milestones-deck.pptx")
        return 0
    else:
        print("❌ Some files are missing")
        print("\nPlease check the setup and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())