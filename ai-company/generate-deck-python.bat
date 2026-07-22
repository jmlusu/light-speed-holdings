@echo off
echo Installing Python dependencies...
pip install -r requirements-pptx.txt

echo Generating milestones deck with Python...
python scripts/generate-milestones-deck.py

echo Done!
pause