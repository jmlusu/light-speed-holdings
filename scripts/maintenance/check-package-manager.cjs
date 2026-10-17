#!/usr/bin/env node
// Package-manager guard for the LightSpeed repo.
//
// The web surface is pinned to `npm` with `package-lock.json` as the
// authoritative lockfile (repo cleanup 2026-10-06, Stage 5). Running
// `bun install` would synthesize a competing `bun.lock` and strand the
// project on a different lockfile, so bun is a hard error here.
// `npm install` is the only supported path.
//
// NOTE: this guard is currently advisory — nothing invokes it yet
// (no preinstall hook, CI step, or docs reference). Wire it in before
// relying on it as enforcement.
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

// Refuse only when bun is identifiable.
if (isBun) {
  console.error('[package-manager] Refusing install: this repo is pinned to `npm`.');
  console.error('[package-manager]   `package-lock.json` is the authoritative lockfile;');
  console.error('[package-manager]   `bun install` would synthesize a competing `bun.lock`.');
  console.error('[package-manager] Install with:  npm install');
  process.exit(1);
}
