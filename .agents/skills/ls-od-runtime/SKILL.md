---
name: ls-od-runtime
description: "Operate the Open Design (od) runtime on Windows: install prerequisites, start and stop the local daemon, query status, inspect the SQLite database, and wire the MCP server into OpenCode. Trigger on: 'od daemon', 'open design runtime', 'start open design', 'od mcp', 'open design setup', 'od status'."
---

# Open Design Runtime

Operational procedure for the local `od` daemon in `open-design/`. Commands verified against `apps/daemon/src/cli.ts` (v0.22.1).

## When To Use

- Installing Open Design prerequisites or repairing a failed Windows install.
- Starting, stopping, or checking the local daemon.
- Inspecting the daemon SQLite database (status, verify, vacuum).
- Wiring the Open Design MCP server into OpenCode (global or project scope).
- Diagnosing a missing build, stale port, or MCP config problem.

Runtime only. Never start an unbounded generation or media job from this skill; generation belongs to the task that owns it, and its output is referenced by artifact filename.

## Prerequisites

- **Node ~24** (`package.json#engines`). Node 22 is not supported; the lockfile and `better-sqlite3` ABI are pinned for 24.
- **pnpm 10.33.2** (`package.json#packageManager`). `corepack enable` fails with EPERM on Windows (cannot write shims under `Program Files`); use `npm install -g pnpm@10.33.2` instead.
- **Visual Studio Build Tools 2022 or newer with the C++ workload.** `better-sqlite3` has no prebuilt win32/Node 24 binary, so `pnpm install` compiles it via node-gyp (~2 minutes). This is expected, not a version conflict.
- macOS, Linux, and WSL2 are the primary supported paths; Windows native is best-effort. In WSL2, a Linux `/usr/bin/od` may shadow the Open Design CLI — keep a WSL-native wrapper earlier in `PATH`.
- The `od` bin (`apps/daemon/bin/od.mjs`) imports `apps/daemon/dist/cli.js` and throws if it is missing. `pnpm install` runs `scripts/postinstall.mjs`, which builds that dist. If it is still missing, run `pnpm bootstrap` (or `pnpm --filter @open-design/daemon build`).

## Daemon Lifecycle

Start:

```bash
od daemon start [--headless] [--serve-web] [--port <n>] [--host <addr>] [--no-open]
```

- Port defaults to `7456` (`OD_PORT`); host defaults to `127.0.0.1` (`OD_BIND_HOST`).
- `--headless` implies `--no-open`. `--serve-web` serves the web UI over the existing port with no Electron and also sets headless.
- `od daemon start` is **foreground and blocking**: it awaits a shutdown promise and handles SIGINT/SIGTERM. In a script, launch it detached (for example `Start-Process`); do not call it synchronously.
- On startup it logs `[od] listening on <url> (headless|desktop)`.

Status and stop:

```bash
od daemon status [--json] [--daemon-url <url>]   # GET /api/daemon/status
od daemon stop [--daemon-url <url>]              # POST /api/daemon/shutdown
```

Database:

```bash
od daemon db status              # SQLite path, size (incl. WAL/SHM), schema version, per-table row counts
od daemon db verify [--quick]    # integrity_check + foreign_key_check
od daemon db vacuum              # SQLite VACUUM
```

Help and exit codes:

```bash
od daemon          # prints usage, exits 2
od daemon --help   # prints usage, exits 0
od daemon <unknown>  # "unknown subcommand: od daemon <sub>", exits 2
```

Do not use root `pnpm dev`, `pnpm start`, or `pnpm daemon`; the repository removed those aliases. The dev-stack lifecycle entry point is `pnpm tools-dev` (`--daemon-port`, `--web-port`), while this skill targets the daemon alone.

## CLI Map

Every key below is a verified `SUBCOMMAND_MAP` entry (`apps/daemon/src/cli.ts:388`). Flags and routes vary per command; run `od <cmd> --help` before using one.

| Command | Scope |
|---|---|
| `agent` | Agent definitions and commands |
| `artifacts` | Artifact catalogue and operations |
| `media` | Media generation dispatch |
| `mcp` | stdio MCP server and agent installer |
| `amr` | AMR agent flows |
| `collab` | Collaboration and multi-agent runs |
| `message-center` | Message center |
| `research` | Research search |
| `plugin` | Plugin management |
| `ui` | UI actions (including `od ui show --schema`) |
| `marketplace` | Marketplace |
| `share` | Share links |
| `brand`, `brands` | Brand resources |
| `project` | Workspace projects |
| `strategy` | Strategy runs |
| `workspace` | Workspace state |
| `automation`, `automations` | Routines and automations |
| `memory` | Agent memory |
| `run` | Runs |
| `files` | Files |
| `templates` | Project snapshots — NOT the design-template catalogue |
| `conversation`, `chat` | Conversations and chat |
| `deploy` | Deploy |
| `daemon` | Daemon lifecycle and database |
| `atoms` | Atoms |
| `skill`, `skills` | Skill catalogue |
| `design-systems` | Design systems |
| `resource` | Resources |
| `craft` | Craft rules |
| `diagnostics` | Diagnostics |
| `export` | Export |
| `lint` | Lint |
| `status` | Status |
| `version` | Version |
| `whats-new` | Changelog |
| `doctor` | Environment doctor |
| `config` | Configuration |
| `library` | Library assets |
| `figma` | Figma integration |

Rendering templates live under `design-templates/` and `/api/design-templates`; functional skills live under `skills/` and `/api/skills`. With no subcommand, `od` starts the daemon and opens the web UI.

## MCP Wiring

Run the stdio server:

```bash
od mcp [--daemon-url <url>]
```

Install into an agent config:

```bash
od mcp install <slug> [--print|--dry-run] [--json] [--name <name>] [--uninstall|--remove] [--daemon-url <url>]
```

- `--print` / `--dry-run` previews without writing; `--json` is machine-readable (dry runs include the launch spec).
- `--name <name>` sets the server name (default `open-design`).
- The launch command is resolved from the running daemon's `/api/mcp/install-info`, so the installed entry matches Settings -> MCP. If the daemon is not running, a minimal `od mcp --daemon-url <url>` is used.
- For OpenCode, `od mcp install opencode` writes the **global** config at `~/.config/opencode/opencode.json` under key `mcp` as `{ type: "local", command: [...], enabled: true }`, then prints `installed <serverName> into <configPath>`.
- A repo-local `opencode.json` (project scope) is not written by the installer; hand-edit it. Global and project config merge.

```bash
od mcp install opencode --print --json   # preview first
od mcp install opencode                  # then write
od mcp install opencode --uninstall      # remove
```

## Windows Failure Modes

| Symptom | Fix |
|---|---|
| `corepack enable` -> EPERM | `npm install -g pnpm@10.33.2` |
| node-gyp / MSB error building `better-sqlite3` | Install VS Build Tools 2022+ with the C++ workload, or use WSL2 |
| `OpenDesign daemon dist entry not found at ...\dist\cli.js` | Run `pnpm bootstrap` or `pnpm --filter @open-design/daemon build` in `open-design` |
| `daemon start` appears hung | It is blocking by design; use `od daemon status --json` from a second shell or launch detached |
| Port 7456 already in use / stale daemon | `od daemon status --json`, then `od daemon stop`, then start again |
| Installer shows `Publisher: Unknown publisher` | SmartScreen: More info -> Run anyway, only for an installer you downloaded yourself |
| Long-path or antivirus locks in `node_modules` | Enable long paths and exclude `node_modules` from real-time scanning, then rerun `pnpm install` |
| `od` in WSL runs the GNU coreutils tool | Put a WSL-native Open Design wrapper earlier in `PATH` |

## Verification

1. `node --version` -> `v24.x`.
2. `pnpm --version` -> `10.33.2`.
3. In `open-design`: `pnpm install` (postinstall builds `apps/daemon/dist`).
4. `node apps/daemon/dist/cli.js version` (use this if `od` is not on `PATH`).
5. `od daemon start --headless` in a separate terminal (blocks).
6. `od daemon status --json` -> running.
7. `od mcp install opencode --print --json` -> preview only.
8. `od daemon stop` when finished.
