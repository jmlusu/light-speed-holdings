# Engineering Standard: Dual-Environment Parity (OpenCode & AI Studio)

## Executive Summary
This document defines the mandatory architecture and code-level specifications required for all monorepo applications to operate seamlessly across both **OpenCode** (Local/Production environment) and **AI Studio** (Managed Cloud Preview environment).

Implementing these standards prevents AI Studio from mutating workspace lockfiles, breaking database extensions, or altering security configurations during platform syncs.

---

## 1. Package Manager Standard (Corepack Enforced `pnpm`)

To prevent AI Studio from stripping `pnpm` workspaces and converting project dependencies to `npm`, all root `package.json` files MUST enforce Corepack and explicit `pnpm` engines.

### Instructions for Agent:
1. Update root `package.json` with explicit `packageManager` and `engines` definitions.
2. Add a `preinstall` hook to force Corepack activation prior to dependency resolution.

```json
{
  "name": "root-monorepo",
  "private": true,
  "engines": {
    "node": ">=22.0.0",
    "pnpm": ">=9.0.0"
  },
  "packageManager": "pnpm@9.15.0",
  "scripts": {
    "preinstall": "npx --yes corepack enable"
  }
}
```

---

## 2. Git Protection Configuration

To ensure lockfiles and workspace configs are never overwritten when merging branches updated by AI Studio back into OpenCode:

### Instructions for Agent:
1. Create or update `.gitattributes` at the root of the repository.
2. Add custom merge driver rules for lockfiles and configuration files.

#### `.gitattributes`
```text
pnpm-lock.yaml merge=ours_lockfile
pnpm-workspace.yaml merge=ours_lockfile
.npmrc merge=ours_lockfile
```

3. Ensure developers and agent setup routines execute the local merge driver initialization script:

#### `scripts/setup-git-hooks.sh`
```bash
#!/usr/bin/env bash
set -e

echo "Setting up custom Git merge drivers for pnpm lockfiles..."
git config merge.ours_lockfile.name "Keep local pnpm lockfile during merges"
git config merge.ours_lockfile.driver "git merge-file --ours %A %O %B"
echo "Git merge drivers successfully configured."
```

---

## 3. Dynamic Application Server Setup (Fastify)

Hardcoding IP bindings (`0.0.0.0`), ports (`3000`), or disabling security headers (CSP) breaks local development and security compliance. Server instances MUST detect environment contexts dynamically.

### Instructions for Agent:
Update Fastify server initialization logic to adapt security headers and network bindings based on environment signals.

```typescript
import Fastify from 'fastify';
import helmet from '@fastify/helmet';

export async function createServer() {
  const app = Fastify({ logger: true });

  const isCloudPreview =
    process.env.AISTUDIO_PREVIEW === 'true' ||
    process.env.NODE_ENV === 'development_cloud';

  // Dynamic Content Security Policy (CSP)
  await app.register(helmet, {
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        // Allow framing inside AI Studio preview if in cloud mode; enforce strict policy locally
        frameAncestors: isCloudPreview
          ? ['https://*.google.com', 'https://*.aistudio.google']
          : ["'none'"]
      }
    }
  });

  return app;
}

export async function startServer(app: ReturnType<typeof Fastify>) {
  const isCloudPreview = process.env.AISTUDIO_PREVIEW === 'true';

  const port = Number(process.env.PORT) || 3000;
  const host = process.env.HOST || (isCloudPreview ? '0.0.0.0' : '127.0.0.1');

  await app.listen({ port, host });
  console.log(`Server running on http://${host}:${port}`);
}
```

---

## 4. Environment-Aware Database Strategy

Applications MUST support both full PostgreSQL with `pgvector` (OpenCode/Production) and embedded `PGlite` (AI Studio preview fallback) without modifying source code.

### Instructions for Agent:
Update the database connection factory to evaluate available connection strings and handle conditional vector extension initialization.

```typescript
import { PGlite } from '@electric-sql/pglite';
import { drizzle as drizzlePg } from 'drizzle-orm/node-postgres';
import { drizzle as drizzlePglite } from 'drizzle-orm/pglite';
import { Pool } from 'pg';

export interface DbConnection {
  db: any;
  isPglite: boolean;
}

export async function initializeDatabase(): Promise<DbConnection> {
  const dbUrl = process.env.DATABASE_URL;

  // Fallback to PGlite if no external DB connection is defined
  if (!dbUrl || process.env.USE_PGLITE === 'true') {
    console.warn('[DB] DATABASE_URL missing or USE_PGLITE flag enabled. Initializing PGlite...');
    const client = new PGlite();
    return {
      db: drizzlePglite(client),
      isPglite: true
    };
  }

  console.log('[DB] Connecting to PostgreSQL database...');
  const pool = new Pool({ connectionString: dbUrl });
  return {
    db: drizzlePg(pool),
    isPglite: false
  };
}

export async function runMigrations(dbInstance: DbConnection) {
  if (dbInstance.isPglite) {
    console.log('[Migrations] Skipping pgvector and native extension DDL for PGlite connection.');
    // Run core schema migrations only
    return;
  }

  console.log('[Migrations] Running full schema migrations including vector extensions...');
  // Run full DDL schema migrations
}
```

---

## 5. Agent Prompt Instructions (Copy-Paste for OpenCode Agents)

When directing AI agents to execute this fix on a target repository, supply the following command instruction:

> **Agent Directive:**
> Read and execute the specifications outlined in `DUAL_ENVIRONMENT_SPEC.md`.
> 1. Enforce Corepack in `package.json` and set `engines.pnpm`.
> 2. Create `.gitattributes` and `scripts/setup-git-hooks.sh` to prevent `pnpm-lock.yaml` overwrites during merges.
> 3. Refactor Fastify server configs to use dynamic host (`HOST`), port (`PORT`), and CSP `frameAncestors` directives.
> 4. Refactor database initialization to dynamically fall back to `PGlite` when `DATABASE_URL` is absent, and conditionally bypass `pgvector` extension setup.
> 5. Verify local build passes with `pnpm build` and `pnpm dev`.
