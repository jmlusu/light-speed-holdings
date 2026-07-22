#!/usr/bin/env node
/**
 * Simple test script to verify Node.js setup
 */

console.log("Node.js version:", process.version);
console.log("Platform:", process.platform);
console.log("Architecture:", process.arch);

// Check if pptxgenjs is installed
try {
  require.resolve("pptxgenjs");
  console.log("✅ pptxgenjs is installed");
} catch (e) {
  console.log("❌ pptxgenjs is not installed");
  console.log("Run: npm install");
}

console.log("\nTo generate the milestones deck:");
console.log("1. Run: npm install");
console.log("2. Run: node scripts/generate-milestones-deck.js");
console.log("3. Or run: npm run generate-deck");
console.log("4. Or double-click: generate-deck.bat");