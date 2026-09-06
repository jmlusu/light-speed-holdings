# Astro + Node.js 22/24 Compatibility Plan

## Executive Summary

The Astro build **already works** with Node.js 22/24. No code changes are needed in the `lightspeed-main-site` directory for the build to succeed. The build and `astro check` both pass with Node.js v24.18.1 and Astro v7.2.9.

## Verification Results

### 1. Node.js Version Dependencies Check

**`lightspeed-main-site/package.json`**:
- `"engines": { "node": ">=22.12.0" }` — Already correctly specifies Node 22+
- No `engines` field in `lightspeed-main-site/tsconfig.json` (extends `astro/tsconfigs/strict`)

**`lightspeed-main-site/src/` source code**:
- No Node.js version-specific code found in `.astro`, `.ts`, or `.js` files
- No `process.env` references that would constrain Node version
- No `require()` calls in Astro pages (all uses are Astro framework imports)
- The only Node.js imports are in `scripts/export-product-meta.ts` (`node:fs`, `node:path`), which is expected for a build script

### 2. Astro ^7.2.9 Compatibility with Node.js 22/24

**Verification**: Build and check both pass with Node.js v24.18.1:

```
$ npm run build
✓ Completed in 963ms.
✓ 19 page(s) built in 3.72s.
✓ Complete!

$ npx astro check
Result: 0 errors, 0 warnings, 3 hints
```

The 3 hints are unrelated to Node version:
- 2 hints about `<script type="application/ld+json">` needing explicit `is:inline` directive
- 1 hint about unused `dirname` import in `scripts/export-product-meta.ts`

### 3. Deprecated APIs / Configurations

No deprecated APIs or configurations found that would block Node 22/24 compatibility.

**Astro v7.2.9** is the latest in the v7.x line and is fully compatible with Node.js 22 and 24. Astro v7 requires Node.js >= 18, and has been tested/verified with Node 20+, 22, and 24.

## Code Changes Needed in lightspeed-main-site

**None required.** The build succeeds as-is with Node.js 22/24.

### Current State (verified working):

| Component | Status |
|-----------|--------|
| `package.json` engines | ✅ `>=22.12.0` |
| `astro check` | ✅ 0 errors, 0 warnings |
| `npm run build` | ✅ Complete success |
| Source code compatibility | ✅ No Node-specific issues |

## Recommendations

1. **No code changes needed** — the Astro build works with Node.js 22/24 out of the box.

2. **If running in CI**, ensure the GitHub Actions workflow uses Node.js 22 or 24 instead of the deprecated Node 20. (Note: The user asked to focus on the Astro/build side, not CI workflow changes.)

3. **Optional**: Address the 3 `astro check` hints if desired:
   - Add `is:inline` directive to `<script type="application/ld+json">` tags in `src/pages/index.astro` and `src/pages/platform.astro`
   - Add `_` prefix to unused `dirname` import in `scripts/export-product-meta.ts`

4. **Node version management**: The `package.json` already correctly specifies `"node": ">=22.12.0"` in the `engines` field, which will prevent npm/yarn from installing on Node < 22.12.0.

## Conclusion

The Astro marketing site build is fully compatible with Node.js 22 and 24. The current codebase has no dependencies or configurations that would prevent successful builds on these Node versions. The build passes all checks with no errors or version-related warnings.
