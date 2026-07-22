@echo off
echo Installing dependencies...
npm install

echo Generating milestones deck...
node scripts/generate-milestones-deck.js

echo Done!
pause