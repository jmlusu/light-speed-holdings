@echo off
echo Installing Python dependencies...
uv sync --extra dev

echo Generating milestones deck with Python...
uv run python scripts/generate-milestones-deck.py

echo Done!
pause