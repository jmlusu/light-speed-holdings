# OpenDesign Monorepo Architecture Report

**Repository:** `C:\Users\jmlus\light-speed-holdings` (also `open-design` subdirectory)
**Date:** Tue Nov 10 2026
**Architect Role:** Senior Monorepo Architect

---

## 1. Workspace Structure

The monorepo uses **pnpm workspaces** as its package manager and module system.

- **Root `package.json`** (`C:\Users\jmlus\light-speed-holdings\package.json`): The top-level project manifest with global dependencies (React 18, Vitest, Playwright, Tailwind CSS, etc.) and scripts (`dev`, `build`, `lint`, `test`, `preview`).

- **`open-design/pnpm-workspace.yaml`** (`C:\Users\jmlus\light-speed-holdings\open-design\pnpm-workspace.yaml`): The pnpm workspace configuration listing four workspace scopes:
  - `packages/*` — shared libraries
  - `apps/*` — application runtimes
  - `tools/*` — developer lifecycle tools
  - `shells/*` — terminal/shell interfaces

- **Workspace root `.package.json`** defines `packageManager: "pnpm@10.33.2"` with strict overrides and `onlyBuiltDependencies` for native deps (better-sqlite3, electron, etc.).

- **Core directories at workspace root:**
  - `apps/` — five application runtimes
  - `packages/` — two packages (design-system, data-use-cases) at root level
  - `tools/` — developer tooling (dev, pack, release, serve)
  - `open-design/` — the primary OpenDesign monorepo (also a pnpm workspace)
  - `.ai-company/` — governance and agent configuration

---

## 2. Package Map

### Root-Level Packages (at `C:\Users\jmlus\light-speed-holdings\`)

| Package | Name | Summary |
|---------|------|---------|
| `design-system` | `@lightspeed/design-system` | LightSpeed Holdings canonical UI components, design tokens, and utilities; provides shared React primitives and Tailwind-based design system for the organization. |
| `data-use-cases` | `@lightspeed/data-use-cases` | Registry, filters, and types for the use case explorer; manages use case data browsing and filtering functionality. |

### OpenDesign Monorepo Packages (at `C:\Users\jmlus\light-speed-holdings\open-design\`)

| Package | Name | Summary |
|---------|------|---------|
| `components` | `@open-design/components` | Shared React UI primitives and primitive CSS; provides foundational UI building blocks consumed by apps; depends on React 18 only. |
| `contracts` | `@open-design/contracts` | Pure TypeScript contracts for the web/daemon boundary; shared DTOs, error shapes, and API contracts between web app and daemon; uses Zod for validation. |
| `sidecar-proto` | `@open-design/sidecar-proto` | OpenDesign sidecar business protocol; owns business action names and DTO/status shapes; does not own process identity or lifecycle mechanics. |
| `sidecar` | `@open-design/sidecar` | Complete business-agnostic sidecar client boundary and protocol implementation; owns five-field identity (`channel`, `namespace`, `source`, `mode`, `app`), private transport, and lifecycle atomics. |
| `platform` | `@open-design/platform` | Generic OS process primitives; includes process-contract serialization, command parsing, process matching/search, and well-known toolchain bin discovery. |
| `agui-adapter` | `@open-design/agui-adapter` | Pure TypeScript bidirectional adapter between OpenDesign's PersistedAgentEvent/GenUIEvent/PluginPipelineStageEvent and the AG-UI canonical event protocol; no Node:fs imports. |
| `launcher-proto` | `@open-design/launcher-proto` | Launcher protocol and path/state primitives; owns channel/version/namespace validation, launcher directory derivation, runtime/cleanup descriptors, target selection, and after-quit argument parsing. |
| `metatool` | `@open-design/metatool` | Internal metadata helpers for checking freshness of built OpenDesign tool dist outputs; reusable hash/check/write mechanics. |
| `registry-protocol` | `@open-design/registry-protocol` | Pure TypeScript registry backend protocol for OpenDesign plugin sources; owns backend list/search/resolve/manifest/doctor schemas. |
| `release` | `@open-design/release` | Open Design release domain primitives; owns release channel names, version parsing/formatting, metadata field derivation, storage prefixes, release namespaces, and app identity data. |
| `diagnostics` | *(mentioned in AGENTS.md)* | Shared diagnostics export primitives for log collection, redaction, manifests, crash-report discovery, and zip packaging used by daemon and desktop. |
| `download` | *(mentioned in AGENTS.md)* | Managed-download runtime; owns resumable and checksum-verified transfers, concurrent-request deduplication, target locking, inspection/removal, copy-and-clear, and pruning. |
| `host` | *(mentioned in AGENTS.md)* | Web/desktop host bridge contract; models renderer-facing host capabilities and helpers while keeping `window.__od__` access out of app UI code. |

### Application Apps (at `C:\Users\jmlus\light-speed-holdings\open-design\apps\`)

| App | Name | Summary |
|-----|------|---------|
| `web` | `@open-design/web` | Next.js 16 App Router + React 18 web runtime; entrypoints in `apps/web/app/`; main client shell at `apps/web/src/App.tsx`; rewrites `/api/*`, `/artifacts/*`, `/frames/*` to `OD_PORT` during local `tools-dev` runs. |
| `daemon` | `@open-design/daemon` | Express + SQLite local daemon and `od` CLI bin; owns REST/SSE APIs (`/api/*`), agent CLI spawning, skills, design systems, artifact persistence, static serving, and daemon-managed data. |
| `desktop` | `@open-design/desktop` | Electron shell; does not guess web port; reads runtime status through sidecar IPC and opens reported web URL. |
| `packaged` | `@open-design/packaged` | Thin packaged Electron runtime entry; starts packaged daemon/web sidecars, registers `od://` entry protocol, delegates desktop host behavior to `apps/desktop`. |
| `closure` | `@open-design/closure` | Independently distributable OpenDesign Closure content; cold-start fixture independent from Web/daemon/Sidecar/shell; emits only public `@open-design/standalone` contribution shapes. |

---

## 3. Dependency Graph

### Internal Package Dependencies (→ means "depends on")

**Shared Libraries →**

```
components → contracts (pure TypeScript contracts only)
components → sidecar-proto (for sidecar business shapes)
components → sidecar (for identity/stamp contracts)
components → platform (for OS process primitives)
components → agui-adapter (for AG-UI event protocol)
components → release (for release DTOs)

contracts → release (workspace:*)
contracts → zod (3.25.76 for validation)

sidecar-proto → release (workspace:*)
sidecar → platform (workspace:*)
sidecar → release (workspace:*)
sidecar → launcher-proto (for launcher protocol)

platform → (no internal deps; generic OS primitives)

agui-adapter → contracts (workspace:*)
launcher-proto → release (workspace:*)
launcher-proto → sidecar-proto (workspace:*)
metatool → zod (3.25.76)
registry-protocol → zod (3.25.76)

release → (no internal deps; primitives only)
```

**Application Apps →**

```
web → @open-design/components (workspace:*)
web → @open-design/contracts (workspace:*)
web → @open-design/host (workspace:*)
web → @open-design/platform (workspace:*)
web → @open-design/sidecar (workspace:*)
web → @open-design/sidecar-proto (workspace:*)
web → @open-design/agui-adapter (for AG-UI integration)
web → openai (6.38.0), anthropic (0.32.1), posthog-js, openai, three, lexical, excalidraw

daemon → @open-design/agui-adapter (workspace:*)
daemon → @open-design/contracts (workspace:*)
daemon → @open-design/diagnostics (workspace:*)
daemon → @open-design/launcher-proto (workspace:*)
daemon → @open-design/platform (workspace:*)
daemon → @open-design/plugin-runtime (workspace:*)
daemon → @open-design/registry-protocol (workspace:*)
daemon → @open-design/release (workspace:*)
daemon → @open-design/sidecar (workspace:*)
daemon → @open-design/sidecar-proto (workspace:*)
daemon → better-sqlite3 (12.10.0, built from source on Windows)
daemon → express (5.2.1), cheerio (1.2.0), hyperframes (0.8.1), jszip (3.10.1)
daemon → kiwi-schema (0.5.0), multer (2.2.0), node-pty (1.1.0), pdf-lib (1.17.1)
daemon → posthog-node (5.34.6), pptxgenjs (4.0.1), prom-prom-client (15.1.3)
daemon → @opentelemetry/api (1.9.1), acorn (8.15.0), blake3-wasm (2.1.5)
daemon → @modelcontextprotocol/sdk (1.29.0)

desktop → @open-design/contracts (workspace:*)
desktop → @open-design/diagnostics (workspace:*)
desktop → @open-design/download (workspace:*)
desktop → @open-design/host (workspace:*)
desktop → @open-design/launcher-proto (workspace:*)
desktop → @open-design/platform (workspace:*)
desktop → @open-design/release (workspace:*)
desktop → @open-design/sidecar (workspace:*)
desktop → @open-design/sidecar-proto (workspace:*)

packaged → @open-design/contracts (workspace:*)
packaged → @open-design/daemon (workspace:*)
packaged → @open-design/desktop (workspace:*)
packaged → @open-design/launcher-proto (workspace:*)
packaged → @open-design/platform (workspace:*)
packaged → @open-design/release (workspace:*)
packaged → @open-design/sidecar (workspace:*)
packaged → @open-design/sidecar-proto (workspace:*)
packaged → @open-design/web (workspace:*)
```

**Root-Level Packages →**

```
data-use-cases → react (18.3.1, peerDependency)
design-system → react (18.3.1), react-dom (18.3.1), clsx, tailwind-peer, jsdom, tailwind-merge peer deps
```

---

## 4. Tech Stack & Tooling

### Languages & Runtime

- **Primary language:** TypeScript 5.7–5.9 (strict mode across all packages)
- **Runtime:** Node.js ~24 (engines field in root package.json and all package.json files)
- **Module system:** ESM (`"type": "module"` across workspace)

### Build Tools

- **pnpm** 10.33.2 as the package manager (corepack enabled, pnpm-lock.yaml locked)
- **esbuild** 0.28.0 — used for fast builds in several packages (components, sidecar-proto, metatool, launcher-proto, packaged, closure)
- **tsc** (TypeScript Compiler) — invoked via `pnpm typecheck` across packages
- **Vite** 6.1.0 — dev server and build for the web app (`apps/web`)
- **Next.js** 16.2.6 — the web app framework (App Router, React 18)

### Testing Frameworks

- **Vitest** 4.1.6 or 5.0.0 — unit and integration tests across packages and apps
- **Playwright** 1.63.0 — end-to-end UI automation (e2e tests in `e2e/`)
- **Jest DOM** 7.0.1 — DOM testing utilities (transitive via @testing-library)

### Key Dependencies by Category

| Category | Packages |
|----------|----------|
| **UI** | react 18.3.1, react-dom 18.3.1, lucide-react 0.475.0/1.16.0, tailwindcss 4.0/4.3.0, tailwind-merge 3.0.1, @formkit/auto-animate, @lexical/react, excalidraw, shiki, thinking-orbs |
| **HTTP & API** | express 5.2.1, undici 7.29.0, openai 6.38.0, anthropic-sdk 0.32.1, posthog-js, posthog-node, @modelcontextprotocol/sdk |
| **Database** | better-sqlite3 12.10.0 (node-gyp compiled), sqlite via daemon |
| **Media & PDF** | nodemailer 6.9.15, pdf-lib 1.17.1, pptxgenjs 4.0.1, jspdf 4.2.1, ffmpeg @ 1.1.0 |
| **Charts & Visuals** | recharts 3.10.1, three 0.185.1, @open-design/components |
| **Auth & Security** | @opentelemetry/api, blake3-wasm, kiwi-schema |
| **DevOps & CI** | playwright 1.63.0, vitest, tsx 4.22.3 |

---

## 5. Integration Points

### External API Integrations

- **OpenAI API** (`openai@6.38.0`) — consumed in `apps/web/src/` for LLM interactions
- **Anthropic SDK** (`0.32.1`) — consumed in `apps/web/src/`
- **Posthog** (`posthog-js` and `posthog-node`) — event tracking from both web and daemon
- **Model SDKs** — `@modelcontextprotocol/sdk` 1.29.0 for MCP integration

**Daemon HTTP API** (`/api/*` routes in `apps/daemon/src/`):
- `/api/health`, `/api/version` — bootstrap metadata in `server.ts`
- Domain routes in `apps/daemon/src/routes/` (active-context, chat, social-share, plugins, terminal, etc.)
- SSE streams for real-time agent communication

**Contract Layer** (`packages/contracts/`):
- Shared DTOs and API types that both daemon and web consume
- Zod schemas for request/response validation
- Exported API surfaces: `/api/connectionTest`, `/api/amrWallet`, `/api/orbit`, `/api/finalize`, `/api/handoff`, `/api/providerModels`, `/api/reasoningExecution`, `/api/research`, `/api/touchpointTestRuntime`

### State Management

- **Sidecar five-field stamp** (`channel`, `namespace`, `source`, `mode`, `app`) — the single source of truth for runtime state, owned by `@open-design/sidecar`
- **Daemon `RUNTIME_DATA_DIR`** — resolved daemon data root; all daemon-owned data paths derive from it (per Daemon data directory contract)
- **Web `OD_PORT`** — proxy port rewriting during `tools-dev` runs
- **Express + SQLite** — daemon persistence layer

### Routing

- **Web App:** Next.js 16 App Router (`apps/web/app/`); pages and routes defined in the app directory structure
- **Daemon:** Express router with semantic route modules in `apps/daemon/src/routes/`; each route module exports `register*Routes` function
- **CLI:** `apps/daemon/src/cli.ts` — subcommand dispatch via `SUBCOMMAND_MAP`; `od <command>` subcommands
- **Sidecar Protocol:** `@open-design/sidecar-proto` defines business action names; `@open-design/sidecar` implements the five-field identity and private transport

### Where New UI/Features Would Be Mounted

1. **Web App Surface:** `apps/web/src/app/` — Next.js App Router entries; add page routes, components, and UI under the app directory
2. **Daemon API:** `apps/daemon/src/routes/<domain>.ts` — new Express route registrar; wire into `src/server.ts`
3. **Shared Contracts:** `packages/contracts/src/api/` or `packages/contracts/src/types.ts` — new DTO types; update both daemon and web consumers
4. **CLI Surface:** `apps/daemon/src/cli.ts` — register new `od <command>` subcommand with `--json` and `--prompt-file` support
5. **Sidecar Protocol:** `packages/sidecar-proto/` or `packages/sidecar/` — if new business action needed
6. **UI Primitives:** `packages/components/src/` — reuse shared components (Button, VisuallyHidden, etc.) or add new primitives
7. **Design System Tokens:** `packages/design-system/` (root-level) — if new tokens/colors/styles needed for LightSpeed branding

### Key Integration Boundary Rules

- **Web must not import daemon private `src/`** — shared contracts live in `packages/contracts`
- **Daemon must not import web app private `src/`** — web/daemon integration belongs behind HTTP APIs and `packages/contracts`
- **New capabilities require three-step closure:** contract type → daemon route → web surface (if applicable) → CLI command
- **Sidecar awareness must stay in `apps/<app>/sidecar`** or desktop sidecar entry wrapper; app business layers must not import sidecar packages or branch on `runtime.mode`, `namespace`, `ipc`, or `source`
- **Packaged runtime paths must be namespace-scoped and independent from daemon/web ports**

---
*Report generated for manual porting of features from external AI Studio instance. No code modifications were made.*
