// LightSpeed Brand Advertising — Generation Brief Generator
// Usage: node brief-generator.js "<art-direction prompt>" "<platform>" "[mode api|local]"
//
// Produces a JSON generation brief for delegation to media-generation-owner subagent.

const fs = require('fs');
const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: node brief-generator.js "<prompt>" "<platform>" "[mode]"\n' +
    'Platforms: linkedin | instagram | instagram-story | facebook | twitter | youtube-display | google-display | website-hero | billboard | flyer | poster | event-banner');
  process.exit(1);
}

const prompt = args[0];
const platform = args[1];
const mode = args[2] || 'api';

// Platform dimensions table (from ls-brand-advertising SKILL.md)
const dimensions = {
  linkedin: '1200x627',
  instagram: '1080x1080',
  'instagram-story': '1080x1920',
  facebook: '1200x628',
  twitter: '1600x900',
  'youtube-display': '300x250|728x90|160x600',
  'google-display': '300x250,728x90,336x280,970x250',
  'website-hero': 'match site breakpoints (1200x~600)',
  billboard: '12:5 or spec from brief',
  flyer: 'A4 (210x297mm) / A3; 300dpi, CMYK or vector preferred',
  poster: 'A4 (210x297mm) / A3; 300dpi, CMYK or vector preferred',
  'event-banner': 'spec from venue'
};

const dims = dimensions[platform] || platform;

// Brand palette (navy, red, cyan, light grey)
const brandPalette = ['#070A40', '#E63946', '#00BFFF', '#F2F2F2'];

// Expiry: end of current year
const expiresAt = new Date();
expiresAt.setFullYear(expiresAt.getFullYear() + 1);
const expiresIso = expiresAt.toISOString();

// Build brief object
const brief = {
  mode: mode,                                  // api (default, 0 local RAM) | local (opt-in, health_check first)
  model: 'gemini-2.5-flash-image',            // nano-banana / Gemini image generation
  prompt: prompt,                              // art-direction briefed prompt
  dimensions: dims,                            // per-platform dimensions string
  brandPalette: brandPalette,                  // [navy, red, cyan, lightGrey]
  clearSpace: 'official logo clear-space rules',
  outputPath: `docs/assets/campaign-${new Date().getFullYear()}-q${Math.ceil(new Date().getMonth()/3)+1}/`,
  expiresAt: expiresIso                        // ISO 8601, end of next year
};

// Output JSON to stdout (for piping to task delegation)
console.log(JSON.stringify(brief, null, 2));

// Also echo a usage summary
console.log(`\nGeneration brief generated for platform: ${platform}`);
console.log(`Dimensions: ${dims}`);
console.log(`Mode: ${mode}`);
console.log(`Brand palette: ${brandPalette.join(', ')}`);
console.log(`Expires: ${expiresIso}`);
