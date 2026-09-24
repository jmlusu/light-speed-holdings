#!/usr/bin/env node
// Package-manager guard for the LightSpeed CLI monorepo (see
// docs/adr/024-dual-environment-compatibility.md and the root
// package.json `packageManager` field).
//
// The web surface is pinned to `bun` to keep `bun.lock` authoritative while
// AI Studio syncs are mirrored back through OpenCode. npm can silently
// regenerate a `package-lock.json` and strand the project on a different
// lockfile, so running `npm install` in this repository is a hard error.
// `bun install` is the only supported path.
'use strict';

const userAgent = process.env.npm_config_user_agent || '';

// bun exports `npm_config_user_agent` and `npm_execpath` for its own lifecycle
// scripts, but bun 1.4.x synthesizes a bogus `npm/undefined` user-agent, so
// the user-agent alone is not a safe classifier. Treat the run as bun when
// either the user-agent is `bun/<ver>` or `npm_execpath` resolves to the bun
// executable (real npm/pnpm/yarn point it at their own CLI entry instead).
const isBun =
  /^bun\/\d/.test(userAgent) ||
  /[\\/]bun(\.exe)?$/i.test(process.env.npm_execpath || '');

// Refuse only when a non-bun manager is identifiable.
if (!isBun) {
  console.error('[package-manager] Refusing install: this repo is pinned to `bun`.');
  console.error('[package-manager]   The `packageManager` field is "bun@1.4.2" and `bun.lock` is the');
  console.error('[package-manager]   authoritative lockfile; `npm install` would synthesize a');
  console.error('[package-manager]   competing `package-lock.json`.');
  console.error('[package-manager] Install with:  bun install');
  process.exit(1);
}
