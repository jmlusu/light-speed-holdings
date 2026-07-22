# Scripts Directory

This directory contains scripts for generating the AI Company Builder milestones deck and other utilities.

## Milestones Deck Generation

### Node.js Version
- `generate-milestones-deck.js` - Main generation script using PptxGenJS
- `test-setup.js` - Test script to verify Node.js setup

### Python Version
- `generate-milestones-deck.py` - Alternative generation script using python-pptx
- `test-setup-python.py` - Test script to verify Python setup

## Usage

### Windows Users
- `generate-deck.bat` - Batch file for Node.js version
- `generate-deck.ps1` - PowerShell script for Node.js version
- `generate-deck-python.bat` - Batch file for Python version
- `generate-deck-python.ps1` - PowerShell script for Python version
- `test-setup-python.bat` - Test Python setup

### Manual Execution
See the main [README-milestones-deck.md](../README-milestones-deck.md) for detailed instructions.

## Dependencies

### Node.js Version
- Node.js v14+
- npm
- PptxGenJS (installed via npm)

### Python Version
- Python v3.7+
- pip
- python-pptx (installed via pip)

## Output

All scripts generate the same PowerPoint presentation:
- `docs/milestones-deck.pptx`

## Verification

To verify that all files are in place:
```bash
# Using Python
python scripts/verify-setup.py

# Or using batch file (Windows)
verify-setup.bat

# Or using PowerShell
.\verify-setup.ps1
```

## Customization

To modify the presentation:
1. Edit the appropriate generation script
2. Re-run the script using the commands above

Both versions produce identical output with the same professional design.