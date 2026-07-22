# AI Company Builder Milestones Deck Generator

This script generates a professional PowerPoint presentation showcasing the major milestones of the AI Company Builder project.

## Prerequisites

### Option 1: Node.js (Recommended)
- Node.js (v14 or higher)
- npm (comes with Node.js)

### Option 2: Python
- Python (v3.7 or higher)
- pip (comes with Python)

## Usage

### Option 1: Node.js

#### Windows (Batch File)
1. Double-click `generate-deck.bat`
2. Wait for dependencies to install and script to run
3. The presentation will be created at `docs/milestones-deck.pptx`

#### Manual Execution
1. Open terminal/command prompt
2. Navigate to the `ai-company` directory
3. Run:
   ```bash
   npm install
   node scripts/generate-milestones-deck.js
   ```

#### PowerShell
1. Right-click `generate-deck.ps1` and select "Run with PowerShell"
2. Or run in PowerShell:
   ```powershell
   .\generate-deck.ps1
   ```

### Option 2: Python

#### Windows (Batch File)
1. Double-click `generate-deck-python.bat`
2. Wait for dependencies to install and script to run
3. The presentation will be created at `docs/milestones-deck.pptx`

#### Manual Execution
1. Open terminal/command prompt
2. Navigate to the `ai-company` directory
3. Run:
   ```bash
   pip install -r requirements-pptx.txt
   python scripts/generate-milestones-deck.py
   ```

#### PowerShell
1. Right-click `generate-deck-python.ps1` and select "Run with PowerShell"
2. Or run in PowerShell:
   ```powershell
   .\generate-deck-python.ps1
   ```

## Presentation Structure

The generated presentation includes 15 slides:

1. **Title Slide** - Project name and key statistics
2. **Executive Summary** - Key metrics and project overview
3. **Project Timeline** - Visual timeline of all milestones
4. **Milestone 1: Foundation** - Core architecture and registry system
5. **Milestone 2: Sprint 1** - Code hardening and audit trail
6. **Milestone 3: Sprint 2** - Core engines and integration
7. **Milestone 4: Organization Expansion** - 53 new roles
8. **Milestone 5: Sprint 3** - Gap closure and testing
9. **Milestone 6: Dashboard & Monitoring** - FastAPI dashboard and KPIs
10. **Milestone 7: CLI & DX** - 26 CLI commands
11. **Milestone 8: Documentation & Governance** - 30+ docs
12. **Quality Metrics** - Test results and quality standards
13. **Architecture Overview** - Module hierarchy
14. **Remaining Work** - Sprint 4 items
15. **Next Steps** - Recommendations

## Design

- **Color Scheme**: Professional dark blue and teal theme
- **Layout**: Clean, modern design with consistent formatting
- **Content**: Bullet points, metric cards, and tables for clarity
- **Typography**: Arial font family for readability

## Output

The presentation is saved to:
```
docs/milestones-deck.pptx
```

## Customization

To modify the presentation:
1. Edit `scripts/generate-milestones-deck.js` (Node.js) or `scripts/generate-milestones-deck.py` (Python)
2. Re-run the script using the appropriate command

The Node.js script uses PptxGenJS library, while the Python script uses python-pptx library.

## Troubleshooting

### Node.js Issues
- If `npm install` fails, try running `npm cache clean --force`
- If Node.js is not found, ensure it's installed and in your PATH

### Python Issues
- If `pip install` fails, try running `pip install --user -r requirements-pptx.txt`
- If Python is not found, ensure it's installed and in your PATH

### Testing Setup
Run the test script to verify your setup:
```bash
# Node.js
node scripts/test-setup.js

# Python
python scripts/test-setup-python.py
```

### Verifying All Files
To verify that all files are in place:
```bash
# Using Python
python scripts/verify-setup.py

# Or using batch file (Windows)
verify-setup.bat

# Or using PowerShell
.\verify-setup.ps1
```